#include <la.hpp>

#include <cuda_runtime_api.h>
#include <cublas_v2.h>
#include <cusparse.h>

#include "cuda_ngstd.hpp"
#include "unifiedvector.hpp"

// own ngsolve cuda-kernels:
extern void SetScalar (double val, int n, double * dev_ptr); 
extern void MultDiagonal (int n, double * D, double * x, double * y);
extern void MultAddDiagonal (int n, double alpha, double * D, double * x, double * y);


extern void ConstEBEKernelCopyIn (int numblocks, int bs, int * row_dnums, double * dev_ux, double * dev_hx);
extern void ConstEBEKernelCopyOut (int numblocks, int bs, int * col_dnums, double * dev_hy, double * dev_uy);



namespace ngla
{
  using namespace ngs_cuda;
  
  
  void InitCuLinalg();
  cublasHandle_t Get_CuBlas_Handle ();

  class DevSparseMatrix;


  /* AutoVector CreateUnifiedVector(size_t size); */

  class DevMatrix : public BaseMatrix
  {
  public:
    DevMatrix() { }

    virtual AutoVector CreateRowVector() const { return make_unique<UnifiedVector>(Width()); }
    virtual AutoVector CreateColVector() const { return make_unique<UnifiedVector>(Height()); }
  };

  shared_ptr<BaseMatrix> CreateDevMatrix (BaseMatrix &mat);
  shared_ptr<BaseMatrix> CreateDevMatrix (Matrix<> &mat);


  class DevSparseMatrix : public DevMatrix
  {
  protected:
    //cusparseMatDescr_t * descr;
    cusparseSpMatDescr_t descr;
    int * dev_ind;
    int * dev_col;
    double * dev_val;
    int height, width, nze;
  public:
    DevSparseMatrix () { }
    DevSparseMatrix (const SparseMatrix<double> & mat);
    virtual ~DevSparseMatrix ();

    // TODO: implement?
    /* virtual shared_ptr<BaseMatrix> InverseMatrix */ 
    /* virtual void MultTransAdd (double s, const BaseVector & x, BaseVector & y) const override; */
    /* // y += s L * x */
    /* virtual void MultAdd1 (const BaseVector & x, BaseVector & y, */ 
    /*                        const BitArray * ainner = NULL, */
    /*                        const Array<int> * acluster = NULL) const override; */

    /* // y += s (D + L^T) * x) */
    /* virtual void MultAdd2 (double s, const BaseVector & x, BaseVector & y, */
    /*                        const BitArray * ainner = NULL, */
    /*                        const Array<int> * acluster = NULL) const override; */


    virtual void Mult (const BaseVector & x, BaseVector & y) const;
    virtual void MultAdd (double s, const BaseVector & x, BaseVector & y) const;
    /* virtual void Scale (double d); */

    /*
    virtual AutoVector CreateRowVector () const
    {
      return UnifiedVector(width).CreateVector();
    }

    virtual AutoVector CreateColVector () const
    {
      return UnifiedVector(height).CreateVector();
    }
    */

    virtual int VHeight() const { return height; }
    virtual int VWidth() const { return width; }
  };


  class DevDiagonalMatrix : public DevMatrix
  {
  protected:
    UnifiedVector diag;

  public:
    DevDiagonalMatrix (UnifiedVector _diag) : diag(_diag) { }

    virtual void Mult (const BaseVector & x, BaseVector & y) const;
    virtual void MultAdd (double s, const BaseVector & x, BaseVector & y) const;

    virtual int VHeight() const { return diag.Size(); }
    virtual int VWidth() const { return diag.Size(); }
  };


  
  class DevConstantElementByElementMatrix : public DevMatrix
  {
    size_t h, w; // big matrix shape

    double * dev_mat;
    size_t hm, wm;  // small matrix shape
    
    DevTable<int> rowdnums, coldnums;
    DevTable<int> row_coloring, col_coloring;

    bool disjoint_rows, disjoint_cols;
    size_t numblocks;
  public:
    DevConstantElementByElementMatrix (const ConstantElementByElementMatrix & mat);
    virtual void MultAdd (double s, const BaseVector & x, BaseVector & y) const;

    virtual int VHeight() const { return h; }
    virtual int VWidth() const { return w; }
  };
  

  
  shared_ptr<DevSparseMatrix> MatMult (const DevSparseMatrix& mata, const DevSparseMatrix& matb);

  // dense device matrix
  class DevDMatrix : public DevMatrix
  {
  private:
    size_t height, width;
    double* dev_data;
    /* cusparseDnMatDescr_t descr; */

  public:
    DevDMatrix ();
    DevDMatrix (size_t height, size_t width);
    DevDMatrix (const Matrix<>& mat);
    DevDMatrix (const DevDMatrix& mat);
    ~DevDMatrix ();

    /* const DevDMatrix & operator= (const Expr<TBxx> & mat) const; */
    const DevDMatrix & operator= (double d) const;
    const DevDMatrix & operator= (const DevDMatrix & mat) const;

    int VHeight() const { return height; }
    int VWidth() const { return width; }

    virtual AutoVector CreateRowVector () const;
    virtual AutoVector CreateColVector () const;

    virtual void Add (const BaseMatrix& b);
    virtual void Scale (double d);
    virtual void Mult (const BaseVector& x, BaseVector& y) const;
    virtual void MultAdd (double s, const BaseVector & x, BaseVector & y) const;

    void SetZero ();

    double* DevData () const;

    virtual ostream & Print (ostream & ost) const;    
  };

  shared_ptr<DevDMatrix> MatMult (const DevDMatrix& mata, const DevDMatrix& matb);

  class DevEBEMatrix : public DevMatrix
  {
  private:
    size_t height, width;
    DevDMatrix devmat;
    Table<int> col_dnums, row_dnums;
    bool disjointrows, disjointcols;
  public:
    DevEBEMatrix (const ConstantElementByElementMatrix& mat);
    ~DevEBEMatrix ();

    virtual AutoVector CreateRowVector () const;
    virtual AutoVector CreateColVector () const;

    void MultAdd (double s, const UnifiedVector & x, UnifiedVector & y);
    /* void Scale (double d); */
  };

  // currently uses Mult and MultAdd of DevSparseMatrix
  class DevJacobiPrecond : public DevSparseMatrix
  {
  private:
    /* cusparseSpMatDescr_t descr; */
    shared_ptr<BitArray> inner;
    double* dev_invdiag;
  public:
    DevJacobiPrecond (const SparseMatrix<double> & amat, 
      shared_ptr<BitArray> ainner=nullptr, bool use_par=true);

    /* DevJacobiPrecond (const JacobiPrecond<double> & amat); */

    virtual ~DevJacobiPrecond ();

    /* void Mult (const BaseVector & x, BaseVector & y) const; */
    /* void MultAdd (double s, const BaseVector & x, BaseVector & y) const; */

    /* int VHeight() const override { return height; } */
    /* int VWidth() const override { return height; } */

  };


  // old version
  /* class DevJacobiPreconditioner : public BaseMatrix */
  /* { */
  /*   // should be like this: */
  /*   // double * dev_diag; */
  /*   // int size; */

  /*   // stored as sparse matrix ... */
  /*   /1* cusparseMatDescr_t * descr; *1/ */

    /* // used to be cusparseMatSpDescr_t... not sure about the difference */
    /* cusparseSpMatDescr_t descr; */
  /*   int * dev_ind; */
  /*   int * dev_col; */
  /*   double * dev_val; */
  /*   int height, width, nze; */
    

  /* public: */
  /*   DevJacobiPreconditioner (const SparseMatrix<double> & mat, const BitArray & freedofs); */
  /*   virtual void Mult (const BaseVector & x, BaseVector & y) const; */
  /*   virtual void MultAdd (double s, const BaseVector & x, BaseVector & y) const; */
  /* }; */

}
