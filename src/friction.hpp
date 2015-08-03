#ifndef FRICTIONCLASSHEADERDEF
#define FRICTIONCLASSHEADERDEF

#include <string>
#include "block.hpp"
#include "cartesian.hpp"
#include "fd.hpp"
#include "fields.hpp"
#include "interface.hpp"
#include "load.hpp"

class friction: public interface
{ friend class outputunit;
    friend class front;
public:
    friction(const char* filename, const int ndim_in, const int mode_in, const std::string material_in,
             const int niface, block**** blocks, const fields& f, const cartesian& cart, const fd_type& fd);
    ~friction();
    virtual void scale_df(const double A);
    virtual void calc_df(const double dt);
    virtual void update(const double B);
    virtual void write_fields();
protected:
    double* du;
    double* dux;
    bool load_file;
    int nloads;
    load** loads;
    double* sn;
    double* s2;
    double* s3;
    void read_load(const std::string filename);
    virtual iffields solve_interface(const boundfields b1, const boundfields b2, const int i, const int j, const double t);
    virtual iffields solve_friction(iffields iffin, double snc, const double z1, const double z2, const int i, const int j, const double t);
    virtual boundchar solve_fs(const double phi, const double eta, const double snc, const int i, const int j, const double t);
};

#endif