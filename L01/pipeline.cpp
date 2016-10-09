#include "pipeline.h"
#include <iostream>
#include <fstream>
#include <sstream>

Register registerFile[16];

Register::Register(void) {

	dataValue = 0;
	registerNumber = -1;
	registerName = "";

}

void Register::update(int registerNumber){
	if( registerNumber != -1 ){
		dataValue = registerFile[registerNumber].dataValue;
		registerNumber = registerNumber;
	}
}

/////////////////////////////
// Instruction Implementation
Instruction::Instruction(void) {

	type = NOP;
	dest = -1;
	src1 = -1;
	src2 = -1;
	stage = NONE;
}

Instruction::Instruction(std::string newInst) {

	std::string buf; 
    	std::stringstream ss(newInst); 
	std::vector<std::string> tokens;
	
    	while (ss >> buf){
		tokens.push_back(buf);
	}

	if(tokens[0] == "ADD")
		type = ADD;
	else if(tokens[0] == "SUB")
		type = SUB;
	else if(tokens[0] == "MULT")
		type = MULT;
	else if(tokens[0] == "DIV")
		type = DIV;
	else if(tokens[0] == "LW")
		type = LW;
	else if(tokens[0] == "SW")
		type = SW;
	else if(tokens[0] == "BNEZ")
		type = BNEZ;
	else
		type = NOP;

	dest = -1;
	src1 = -1;
	src2 = -1;

	if(tokens.size() > 1) {
		dest = atoi(tokens[1].erase(0,1).c_str());
	}
	if(tokens.size() > 2) {
		src1 = atoi(tokens[2].erase(0,1).c_str());
	}
	if(tokens.size() > 3) {
		src2 = atoi(tokens[3].erase(0,1).c_str());
	}

	// Store and BNEZ has 2 source operands and no destination operand
	if (type == SW || type == BNEZ) {
		src2 = src1;
		src1 = dest;
		dest = -1;
	}

	stage = NONE;
}
/////////////////////////////

/////////////////////////////
// Application Implementation
Application::Application(void) {

	PC = 0;

}

void Application::loadApplication(std::string fileName) {

	std::string sLine = "";
	Instruction *newInstruction;
	std::ifstream infile;
	infile.open(fileName.c_str(), std::ifstream::in);
	
	if ( !infile ) {
		std::cout << "Failed to open file " << fileName << std::endl;
		return;
	}	

	while (!infile.eof())
	{
		getline(infile, sLine);
		if(sLine.empty())
			break;
		newInstruction = new Instruction(sLine);
		instructions.push_back(newInstruction);
	}

	infile.close();
	std::cout << "Read file completed!!" << std::endl;
	
	printApplication();

}

void Application::printApplication(void) {

	std::cout << "Printing Application: " << std::endl;
	std::vector<Instruction*>::iterator it;
	for(it=instructions.begin(); it < instructions.end(); it++) {
	
		(*it)->printInstruction();
		std::cout << std::endl;
	}

}

Instruction* Application::getNextInstruction() {

	Instruction *nextInst = NULL;

	if( PC < instructions.size() ){
		nextInst = instructions[PC];
		PC += 1;
	}
	
	if( nextInst == NULL )
		nextInst = new Instruction();
	
	return nextInst;
}
/////////////////////////////

/////////////////////////////
// Pipeline Stage
PipelineStage::PipelineStage(void) {
	inst = new Instruction();
	stageType = NONE;	
}

void PipelineStage::clear() {
	inst = NULL;
}

void PipelineStage::addInstruction(Instruction *newInst) {
	inst = newInst;
	inst->stage = stageType;
}
/////////////////////////////

/////////////////////////////
//PipelineStageRegister
PipelineStageRegister::PipelineStageRegister(void){
	inst = new Instruction();
	stageType = NONE;
	rs = new Register(); rs->registerName = "Rs";
	rt = new Register(); rt->registerName = "Rt";
	rd = new Register(); rd->registerName = "Rd";
}

void PipelineStageRegister::clear(){
	inst = NULL;
	rs = NULL;
	rt = NULL;
	rd = NULL;
}
/////////////////////////////

/////////////////////////////
// Pipeline Implementation
Pipeline::Pipeline(Application *app) {

	pipeline[FETCH].stageType = FETCH;
	pipeline[DECODE].stageType = DECODE;
	pipeline[EXEC].stageType = EXEC;
	pipeline[MEM].stageType = MEM;
	pipeline[WB].stageType = WB;
	cycleTime = 0;

	//No FETCH Register// IF/ID maps to ID// ID/EXEC maps to EXEC // EXEC/MEM maps to MEM // MEM/WB maps to WB
	pipelineStageRegister[DECODE].stageType = DECODE;
	pipelineStageRegister[EXEC].stageType = EXEC;
	pipelineStageRegister[MEM].stageType = MEM;
	pipelineStageRegister[WB].stageType = WB;

	printPipeline();

	application = app;

	forwarding = false;

}

bool Pipeline::hasDependency(void) {

	if(pipeline[DECODE].inst->type == NOP)
		return false;

	// Checks if dependency exist between Decode stage and Exec, Mem, WB stage
	for(int i = EXEC; i <= WB; i++) {

		if( pipeline[i].inst == NULL )
			continue;		

		if( pipeline[i].inst->type == NOP )
			continue;

		if( (pipeline[i].inst->dest != -1) && 
		    (pipeline[i].inst->dest == pipeline[DECODE].inst->src1 ||
		     pipeline[i].inst->dest == pipeline[DECODE].inst->src2) ) {
			return true;
		}

	}

	return false;

}

bool Pipeline::forward(){
	if(pipeline[DECODE].inst == NULL)//NULL instruction means no dependency so continue execution
		return true;
	if(pipeline[DECODE].inst->type == NOP)//NOP instruction means no dependency so continue execution
		return true;


	//Forwarding logic //Always forward the most recent value
	if(pipeline[MEM].inst->dest != -1 &&
			( pipeline[MEM].inst->dest == pipeline[DECODE].inst->src1 ) ||
			( pipeline[MEM].inst->dest == pipeline[DECODE].inst->src2 )
		){//Dependency detected between ID/EX and EX/MEM stage
		if(pipeline[MEM].inst->type == LW){//LW instructions forward at MEM/WB stage
			return false;
		}else{
			//Forward correct values
			return true;
		}
	}else if(pipeline[WB].inst->dest != -1 &&
			( pipeline[WB].inst->dest == pipeline[DECODE].inst->src1 ) ||
			( pipeline[WB].inst->dest == pipeline[DECODE].inst->src2 )
		){//Dependency detected between ID/EX and MEM/WB stage

		//Forward correct values
		return true;
	}

	//Forwarding logic
	/*if(pipeline[MEM].inst->dest != -1 && ( pipeline[MEM].inst->dest == pipeline[DECODE].inst->src1 ) ){//Dependency on first operand
		if(pipeline[MEM].inst->type == LW){//LW instructions have to wait until the end of MEM stage
			return false;
		}else if(pipeline[MEM].inst->type == SW){// Data operand of SW is forwarded from EX stage
			if(pipeline[DECODE].inst->type == LW){// LW has to wait for MEM stage to finish before value can be forwarded
				return false;
			}else{//Every instruction can proceed
				return true;
			}
		}else{
			//Update ID/EX register with forwarded value
			return true;
		}
	}else if(pipeline[MEM].inst->dest != -1 && ( pipeline[MEM].inst->dest == pipeline[DECODE].inst->src2 ) ){//Dependency on second operand
		if(pipeline[MEM].inst->type == LW){//LW instructions have to wait until the end of MEM stage
			return false;
		}else if(pipeline[MEM].inst->type == SW){// Address operand of SW is forwarded from EX
			if(pipeline[DECODE].inst->type == LW){// LW has to wait for MEM stage to finish before value can be forwarded
				return false;
			}else{//Every instruction can proceed
				return true;
			}
		}else{
			//Update ID/EX register with forwarded value
			return true;
		}
	}else if( pipeline[WB].inst->dest != -1 && ( pipeline[WB].inst->dest == pipeline[DECODE].inst->src1 ) ){//Dependency on first operand
		//Update ID/EX register with forwarded value

		return true;
	}else if( pipeline[WB].inst->dest != -1 && ( pipeline[WB].inst->dest == pipeline[DECODE].inst->src2 ) ){//Dependency on second operand
		//Update ID/EX register with forwarded value
		return true;
	}*/

	//if no dependency do not change the ID/EX register
	return true;
}

void Pipeline::cycle(void) {
	cycleTime += 1;

	// Writeback
	pipeline[WB].clear();//Clear earlier instruction
	pipeline[WB].addInstruction(pipeline[MEM].inst);//Add new instruction

	// Mem
	pipeline[MEM].clear();//Clear earlier instruction
	pipeline[MEM].addInstruction(pipeline[EXEC].inst);//Add new instruction
	
	// Exec
	// Check for data hazards
	if(this->forwarding){
		pipeline[EXEC].clear();//Clear earlier instruction
		if(!forward()){//Check if forwarding is possible
			pipeline[EXEC].addInstruction(new Instruction());
			return;
		}
		pipeline[EXEC].addInstruction(pipeline[DECODE].inst);
	}else if(!this->forwarding){
		pipeline[EXEC].clear();//Clear earlier instruction
		if(hasDependency()){//Stall if dependency detected
			pipeline[EXEC].addInstruction(new Instruction());
			return;
		}
		pipeline[EXEC].addInstruction(pipeline[DECODE].inst);//Add new instruction
	}

	
	// Decode 
	pipeline[DECODE].clear();//Clear earlier instruction
	pipeline[DECODE].addInstruction(pipeline[FETCH].inst);//Add new instruction
	pipelineStageRegister[EXEC].inst = pipelineStageRegister[DECODE].inst; //Prepare ID/EX Register
	pipelineStageRegister[EXEC].rs->update(pipelineStageRegister[EXEC].inst->src1);
	pipelineStageRegister[EXEC].rt->update(pipelineStageRegister[EXEC].inst->src2);
	//pipelineStageRegister[EXEC].rd->update(pipelineStageRegister[EXEC].inst->dest);
	
	// Fetch
	pipeline[FETCH].clear();//Clear earlier instruction
	pipeline[FETCH].addInstruction(application->getNextInstruction());//Add new instruction
	pipelineStageRegister[DECODE].inst = pipeline[FETCH].inst;//Prepare IF/ID
}

bool Pipeline::done() {

	for(int i = 0; i < 5; i++) {

		if(pipeline[i].inst->type != NOP)
			return false;

	}


	return true;

}

void Pipeline::printPipeline(void) {

	if(cycleTime == 0)
		std::cout << "Cycle" << "\tIF" << "\t\tID" << "\t\tEXEC" << "\t\tMEM" << "\t\tWB" << std::endl;
	std:: cout << cycleTime; 
	for(int i = 0; i < 5; i++) {
		
		pipeline[i].printStage();

	}
	std::cout << std::endl;
}

void PipelineStage::printStage(void) {

	std::cout << "\t";
	inst->printInstruction();

}

void Instruction::printInstruction(void) {
	if(type == NOP)
		std::cout << instructionNames[type] << "         ";
	else if(type == SW || type == BNEZ)
		std::cout << instructionNames[type] << " r" << src1 << " r" << src2;
	else if(type == LW)
		std::cout << instructionNames[type] << " r" << dest << " r" << src1;
	else 
		std::cout << instructionNames[type] << " r" << dest << " r" << src1 << " r" << src2;
}
