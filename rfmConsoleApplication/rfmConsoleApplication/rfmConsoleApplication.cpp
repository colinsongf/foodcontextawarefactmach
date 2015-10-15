// rfmConsoleApplication.cpp : Defines the entry point for the console application.
//



#include "stdafx.h"
#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <string>
#include <iterator>
#include <algorithm>
#include <iomanip>
#include <assert.h>

#include "util/util.h"
#include "util/cmdline.h"
#include "fm_core/fm_model.h"
#include "libfm/src/Data.h"
#include "libfm/src/fm_learn.h"
#include "libfm/src/fm_learn_sgd.h"
#include "libfm/src/fm_learn_sgd_element.h"
#include "libfm/src/fm_learn_sgd_element_adapt_reg.h"
#include "libfm/src/fm_learn_mcmc_simultaneous.h"

#define DATA_DIR "Data\\"
#define RESULTS_DIR	"Results\\"
#define STATS_EXT ".csv"
#define RESULTS_EXT ".txt"

#define PROCESS_EXECUTION_MODE 1

using namespace std;


int executeFM(string train_filename, string test_filename, int k, int learn_iter, int ix) {
	std::ostringstream stringStream;
	string stats_filename, results_filename;
	string k_string;
	string aux_str;
	int aux_idx;
	// Make k part of the string
	stringStream.str("");
	stringStream << "k" << k;
	/* Make the replacement for stats filepath*/
	stats_filename = train_filename;
	// Replace dir Data/ -> Results/
	aux_str = DATA_DIR;
	stats_filename = stats_filename.replace(stats_filename.find(aux_str.c_str(), 0), aux_str.length(), RESULTS_DIR);
	// Replace base.lib extension for csv
	aux_str = "base.libfm";
	if ((aux_idx = stats_filename.find(aux_str.c_str(), 0)) < 0) {
		aux_str = "base";
		stats_filename.find(aux_str.c_str(), 0);
	}
	stringStream << STATS_EXT;
	k_string = stringStream.str();
	stats_filename = stats_filename.replace(stats_filename.find(aux_str.c_str(), 0), aux_str.length(), k_string);
	std::cout << "Stats file path is " << stats_filename << endl;
	/* Make the replacement for results filepath*/
	results_filename = stats_filename;
	aux_str = STATS_EXT;
	results_filename = results_filename.replace(results_filename.find(aux_str.c_str(), 0), aux_str.length(), RESULTS_EXT);
	std::cout << "Results file path is " << stats_filename << endl;
	srand(time(NULL));
	try {
		stringStream.str("");
		std::cout << "Loading train dataset...\t" << endl;
		Data train(0, 0, 1);
		train.load(train_filename);
		train.debug();
		Data test(0, 0, 1);
		std::cout << "Loading test dataset... \t" << endl;
		test.load(test_filename);
		test.debug();
		Data* validation = NULL;
		DVector<RelationData*> relation;
		// (1.2) Load relational data
		{
			vector<string> rel = {};
			// std::cout << "#relations: " << rel.size() << endl;
			relation.setSize(rel.size());
			train.relation.setSize(rel.size());
			test.relation.setSize(rel.size());
			for (uint i = 0; i < rel.size(); i++) {
				relation(i) = new RelationData(0, true, false);
				relation(i)->load(rel[i]);
				train.relation(i).data = relation(i);
				test.relation(i).data = relation(i);
				train.relation(i).load(rel[i] + ".train", train.num_cases);
				test.relation(i).load(rel[i] + ".test", test.num_cases);
			}
		}
		// std::cout << "Loading meta data...\t" << endl;
		// (main table)
		uint num_all_attribute = max(train.num_feature, test.num_feature);
		if (validation != NULL) {
			num_all_attribute = max(num_all_attribute, (uint)validation->num_feature);
		}
		DataMetaInfo meta_main(num_all_attribute);
		// meta_main.loadGroupsFromFile(cmdline.getValue(param_meta_file));

		// build the joined meta table
		for (uint r = 0; r < train.relation.dim; r++) {
			train.relation(r).data->attr_offset = num_all_attribute;
			num_all_attribute += train.relation(r).data->num_feature;
		}
		DataMetaInfo meta(num_all_attribute);
		{
			meta.num_attr_groups = meta_main.num_attr_groups;
			for (uint r = 0; r < relation.dim; r++) {
				meta.num_attr_groups += relation(r)->meta->num_attr_groups;
			}
			meta.num_attr_per_group.setSize(meta.num_attr_groups);
			meta.num_attr_per_group.init(0);
			for (uint i = 0; i < meta_main.attr_group.dim; i++) {
				meta.attr_group(i) = meta_main.attr_group(i);
				meta.num_attr_per_group(meta.attr_group(i))++;
			}

			uint attr_cntr = meta_main.attr_group.dim;
			uint attr_group_cntr = meta_main.num_attr_groups;
			for (uint r = 0; r < relation.dim; r++) {
				for (uint i = 0; i < relation(r)->meta->attr_group.dim; i++) {
					meta.attr_group(i + attr_cntr) = attr_group_cntr + relation(r)->meta->attr_group(i);
					meta.num_attr_per_group(attr_group_cntr + relation(r)->meta->attr_group(i))++;
				}
				attr_cntr += relation(r)->meta->attr_group.dim;
				attr_group_cntr += relation(r)->meta->num_attr_groups;
			}
			meta.debug();

		}
		meta.num_relations = train.relation.dim;
		// (2) Setup the factorization machine
		fm_model fm;
		{
			fm.num_attribute = num_all_attribute;
			fm.init_stdev = 0.1;
			// set the number of dimensions in the factorization
			{
				vector<int> dim = { 1, 1, k };
				assert(dim.size() == 3);
				fm.k0 = dim[0] != 0;
				fm.k1 = dim[1] != 0;
				fm.num_factor = dim[2];
			}
			fm.init();
		}
		// Setup the learning method:
		fm_learn* fml;
		fm.w.init_normal(fm.init_mean, fm.init_stdev);
		fml = new fm_learn_mcmc_simultaneous();
		fml->validation = validation;
		((fm_learn_mcmc*)fml)->num_iter = learn_iter;
		((fm_learn_mcmc*)fml)->num_eval_cases = test.num_cases;
		((fm_learn_mcmc*)fml)->do_sample = true;
		((fm_learn_mcmc*)fml)->do_multilevel = true;
		fml->fm = &fm;
		fml->max_target = train.max_target;
		fml->min_target = train.min_target;
		fml->task = 0;
		fml->meta = &meta;
		// std::cout << "Opening output file" << endl;
		RLog* rlog = NULL;
		ofstream* out_rlog = NULL;
		out_rlog = new ofstream(stats_filename);
		if (!out_rlog->is_open())	{
			throw "Unable to open file " + stats_filename;
		}
		// std::cout << "logging to " << r_log_str.c_str() << endl;
		rlog = new RLog(out_rlog);
		// 
		fml->log = rlog;
		fml->init();
		// set the regularization; for als and mcmc this can be individual per group
		vector<double> reg = {};
		assert((reg.size() == 0) || (reg.size() == 1) || (reg.size() == 3) || (reg.size() == (1 + meta.num_attr_groups * 2)));
		if (reg.size() == 0) {
			fm.reg0 = 0.0;
			fm.regw = 0.0;
			fm.regv = 0.0;
			((fm_learn_mcmc*)fml)->w_lambda.init(fm.regw);
			((fm_learn_mcmc*)fml)->v_lambda.init(fm.regv);
		}
		else if (reg.size() == 1) {
			fm.reg0 = reg[0];
			fm.regw = reg[0];
			fm.regv = reg[0];
			((fm_learn_mcmc*)fml)->w_lambda.init(fm.regw);
			((fm_learn_mcmc*)fml)->v_lambda.init(fm.regv);
		}
		else if (reg.size() == 3) {
			fm.reg0 = reg[0];
			fm.regw = reg[1];
			fm.regv = reg[2];
			((fm_learn_mcmc*)fml)->w_lambda.init(fm.regw);
			((fm_learn_mcmc*)fml)->v_lambda.init(fm.regv);
		}
		else {
			fm.reg0 = reg[0];
			fm.regw = 0.0;
			fm.regv = 0.0;
			int j = 1;
			for (uint g = 0; g < meta.num_attr_groups; g++) {
				((fm_learn_mcmc*)fml)->w_lambda(g) = reg[j];
				j++;
			}
			for (uint g = 0; g < meta.num_attr_groups; g++) {
				for (int f = 0; f < fm.num_factor; f++) {
					((fm_learn_mcmc*)fml)->v_lambda(g, f) = reg[j];
				}
				j++;
			}
		}
		if (rlog != NULL) {
			rlog->init();
		}
		fm.debug();
		fml->debug();
		// () learn		
		fml->learn(train, test);
		std::cout << "Save prediction" << endl;
		DVector<double> pred;
		pred.setSize(test.num_cases);
		fml->predict(test, pred);
		pred.save(results_filename);
	}
	catch (string &e) {
		cerr << endl << "ERROR: " << e << endl;
	}
	catch (char const* &e) {
		cerr << endl << "ERROR: " << e << endl;
	}
	
	return 0;
}


int processDataset(string dataset, bool binary_mode, bool libsvm_format, int iteration, int max_iter, bool prepare_data) {
	std::ostringstream stringStream, filenameStream;
	string cmd_line, train_filename, test_filename, aux_str;
	string out_filename, rlog_filename;

	for (int ix = iteration; ix <= max_iter; ix++) {
		filenameStream.str("");
		stringStream.str("");
		std::cout << "*****************************************" << endl;
		std::cout << "	Iteration " << ix << " on " << dataset << endl;
		std::cout << "*****************************************" << endl;
		if (prepare_data) {
			std::cout << "Preparing Files with Tool: prepare_files.py (Python)" << endl;
			stringStream << "python Tools\\prepare_files.py " << dataset << " 50 " << ix;
			cmd_line = stringStream.str();
			std::cout << cmd_line << endl;
			system(cmd_line.c_str());
		}
		stringStream.str("");
		if (libsvm_format) {
			filenameStream << dataset << "." << ix << ".base";
			train_filename = filenameStream.str();
			filenameStream.str("");
			filenameStream << dataset << "." << ix << ".test";
			test_filename = filenameStream.str();

			aux_str = DATA_DIR;
			string destination_filename = train_filename;
			destination_filename.replace(train_filename.find(aux_str, 0), aux_str.length(), "");
			stringStream.str("");
			stringStream << "ren " << train_filename << " " << destination_filename << ".libfm";
			cmd_line = stringStream.str();
			std::cout << cmd_line << endl;
			system(cmd_line.c_str());

			destination_filename = test_filename;
			destination_filename.replace(test_filename.find(aux_str, 0), aux_str.length(), "");
			stringStream.str("");
			stringStream << "ren " << test_filename << " " << destination_filename << ".libfm";
			cmd_line = stringStream.str();
			std::cout << cmd_line << endl;
			system(cmd_line.c_str());
		} else {
				std::cout << "Converting Files to libFM format with Tool: triple_format_to_libfm.pl (Perl)" << endl;
				filenameStream << dataset << "." << ix << ".base";
				train_filename = filenameStream.str();
				filenameStream.str("");
				filenameStream << dataset << "." << ix << ".test";
				test_filename = filenameStream.str();
				stringStream << "C:\\Perl64\\bin\\perl.exe Tools/triple_format_to_libfm.pl -in " << train_filename << "," << test_filename << " -target 2 -separator \\t";
				cmd_line = stringStream.str();
				std::cout << cmd_line << endl;
				system(cmd_line.c_str());
		}
		std::cout << "Analysing Epicurious with k=5,10,15,20,25" << endl;
		std::cout << "Considering 100 learning iterations" << endl;
		if (binary_mode) {
			std::cout << "Converting files to binary format" << endl;
			stringStream.str("");
			stringStream << "Tools\\convert.exe --ifile " << train_filename << ".libfm --ofilex " << train_filename << ".x --ofiley " << train_filename << ".y";
			cmd_line = stringStream.str();
			system(cmd_line.c_str());
			stringStream.str("");
			stringStream << "Tools\\convert.exe --ifile " << test_filename << ".libfm --ofilex " << test_filename << ".x --ofiley " << test_filename << ".y";
			cmd_line = stringStream.str();
			system(cmd_line.c_str());
			std::cout << "Transposing binary format" << endl;
			stringStream.str("");
			stringStream << "Tools\\transpose.exe --ifile " << train_filename << ".x --ofile " << train_filename << ".xt";
			cmd_line = stringStream.str();
			system(cmd_line.c_str());
			stringStream.str("");
			stringStream << "Tools\\transpose.exe --ifile " << test_filename << ".x --ofile " << test_filename << ".xt";
			cmd_line = stringStream.str();
			system(cmd_line.c_str());
		} else {
			train_filename.append(".libfm");
			test_filename.append(".libfm");
		}
		std::cout << "Test filename is:" << test_filename << endl;
		std::cout << "Train filename is:" << train_filename << endl;
		int kx = 5;
		while (kx <= 25) {
			if (PROCESS_EXECUTION_MODE) {
				// Results/epi_results.txt
				stringStream.str("");
				stringStream << dataset << "." << ix << ".k" << kx << ".txt";
				out_filename = stringStream.str();
				aux_str = DATA_DIR;
				out_filename = out_filename.replace(out_filename.find(aux_str.c_str(), 0), aux_str.length(), RESULTS_DIR);
				// Results/epi_stats.csv
				stringStream.str("");
				stringStream << dataset << "." << ix << ".k" << kx << ".csv";
				rlog_filename = stringStream.str();
				aux_str = DATA_DIR;
				rlog_filename = rlog_filename.replace(rlog_filename.find(aux_str.c_str(), 0), aux_str.length(), RESULTS_DIR);
				stringStream.str("");
				// MCMC
				stringStream << "Tools\\libfm.exe -task r -train " << train_filename << " -test " << test_filename << " -dim ’1,1," << kx << "' -iter 100 -out " << out_filename << " -rlog " << rlog_filename << " -verbosity 1 -method mcmc -init_stdev 0.1";
				// SGD
				// stringStream << "Tools\\libfm.exe -task r -train " << train_filename << " -test " << test_filename << " -dim ’1,1," << kx << "' -iter 500 -out " << out_filename << " -rlog " << rlog_filename << " -verbosity 1 " << "-method sgd -learn_rate 0.01 -regular ’0,0,0.01’ -init_stdev 0.1";
				// ALS
				// stringStream << "Tools\\libfm.exe -task r -train " << train_filename << " -test " << test_filename << " -dim ’1,1," << kx << "' -iter 500 -out " << out_filename << " -rlog " << rlog_filename << " -verbosity 1 " << "-method als -regular ’0,0,0.010’ -init_stdev 0.1";				
				cmd_line = stringStream.str();
				system(cmd_line.c_str());
			}
			else {
				executeFM(train_filename, test_filename, kx, 50, ix);
			}
			if (kx == 5)
				kx = 25;
			else kx = 1000;
		}
	} // ..for
	return 0;
}

int main(int argc, char** argv){
	string epi_filepath = "Data/epicurious";
	string food_filepath = "Data/food";
	int iter = 1;
	if (argv[2] != NULL) {
		iter = atol(argv[2]);
	}
	cout << "argv[1]: string dataset - What is the name of the base dataset?" << endl;
	cout << "argv[2]: bool binary_mode - Will you want to convert to libFM binary format for MF processing?" << endl;
	cout << "argv[3]: bool libsvm_format - Is the base dataset file already in libSVM format?" << endl;
	cout << "argv[4]: int iteration - What will be the first test iteration? (1-...)" << endl;
	cout << "argv[5]: int max iteration - What will be the end iteration? (...-25??)" << endl;
	cout << "argv[5]: bool prepare_data - Do you need to shuffle and split (Train 50% - Test 50%) the dataset?" << endl;
	cout << "Processing file: " << argv[1] << " starting on iteration " << iter << endl;
	
	processDataset(argv[1], (atol(argv[2])>0) ? true : false, (atol(argv[3])>0) ? true : false, atol(argv[4]), atol(argv[5]), (atol(argv[6])>0) ? true : false);
	std::cout << "PROCESSING ENDED SUCCESSFULLY" << endl;
	return 0;
}