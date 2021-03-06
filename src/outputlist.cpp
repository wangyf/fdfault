#include <iostream>
#include <fstream>
#include <string>
#include "domain.hpp"
#include "outputlist.hpp"
#include "outputunit.hpp"
#include <mpi.h>

using namespace std;

outputlist::outputlist(const char* filename, const string probname, const string datadir, const int nt, const domain& d) {
    // constructor
    
    rootunit = 0;
    
    outputunit* cunit = rootunit;
    outputunit* nunit;
    
    // reads input from outlist in input file
    
    bool inputstart;
    string line, name, field;
    int tm, tp, ts, xm[3], xp[3], xs[3];
    
    // open input file, find appropriate place and read in parameters
    
    ifstream paramfile(filename, ifstream::in);
    if (paramfile.is_open()) {
        // scan to start of outputlist
        while (getline(paramfile,line)) {
            if (line == "[fdfault.outputlist]") {
                break;
            }
        }
        if (paramfile.eof()) {
            cerr << "Error reading outputlist from input file\n";
            MPI_Abort(MPI_COMM_WORLD,-1);
        } else {
            // read next output unit
            while (getline(paramfile, line)) {
                if (line.empty()) {
                    break;
                } else {
                    // read in next item
                    name = line;
                    paramfile >> field;
                    paramfile >> tm;
                    paramfile >> tp;
                    paramfile >> ts;
                    for (int i=0; i<3; i++) {
                        paramfile >> xm[i];
                        paramfile >> xp[i];
                        paramfile >> xs[i];
                    }
                    // skip over newline
                    getline(paramfile, line);
                    // traverse list and add onto end
                    cunit = new outputunit(probname, datadir, nt, tm, tp, ts, xm, xp, xs, field, name, d);
                    if (!rootunit) {
                        rootunit = cunit;
                        nunit = rootunit;
                    } else {
                        nunit->set_next_unit(cunit);
                        nunit = nunit->get_next_unit();
                    }
                }
            }
        }
    } else {
        cerr << "Error opening input file in outputlist.cpp\n";
        MPI_Abort(MPI_COMM_WORLD,-1);
    }
    paramfile.close();
	
}

outputlist::~outputlist() {
    
    outputunit* ounit = rootunit;
    outputunit* cunit = rootunit;
    
    while (ounit) {
        cunit = cunit->get_next_unit();
        delete ounit;
        ounit = cunit;
    }
}

void outputlist::write_list(const int tstep, const double dt, const domain& d) {
    // writes outputlist units
    
    outputunit* cunit = rootunit;
    
    // traverse list, calling write_unit for each
    
    while (cunit) {
        cunit->write_unit(tstep,dt,d);
        cunit = cunit->get_next_unit();
    }
    
}

void outputlist::close_list() {
    // writes outputlist units
    
    outputunit* cunit = rootunit;
    
    // traverse list, calling close_file for each
    
    while (cunit) {
        cunit->close_file();
        cunit = cunit->get_next_unit();
    }
}