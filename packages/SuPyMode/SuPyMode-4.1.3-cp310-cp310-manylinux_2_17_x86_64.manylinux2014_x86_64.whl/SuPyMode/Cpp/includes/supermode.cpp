#pragma once

#include "definitions.cpp"
#include "utils.cpp"
#include "numpy_interface.cpp"


struct SuperMode
{
  VectorType Betas, EigenValues, Index;
  size_t ITRLength, Nx, Ny, mode_number, sMode;
  std::string left_boundary, right_boundary, top_boundary, bottom_boundary;
  MatrixType Fields, Coupling, Adiabatic;

  SuperMode(size_t mode_number){this->mode_number = mode_number;}
  SuperMode(){}


  void Init(size_t &ITRLength,
            size_t &Nx,
            size_t &Ny,
            std::string &left_boundary,
            std::string &right_boundary,
            std::string &top_boundary,
            std::string &bottom_boundary,
            int sMode)
  {
    this->Nx             = Nx;
    this->Ny             = Ny;
    this->sMode          = sMode;
    this->ITRLength      = ITRLength;
    this->Fields         = MatrixType(Nx * Ny, ITRLength);
    this->Betas          = VectorType(ITRLength);
    this->EigenValues    = VectorType(ITRLength);
    this->Index          = VectorType(ITRLength);
    this->Adiabatic      = MatrixType(sMode, ITRLength);
    this->Coupling       = MatrixType(sMode, ITRLength);
    this->bottom_boundary = bottom_boundary;
    this->top_boundary    = top_boundary;
    this->right_boundary  = right_boundary;
    this->left_boundary   = left_boundary;
  }

  void copy_other_slice(SuperMode& Other, size_t Slice)
  {
      this->Fields.col(Slice) = Other.Fields.col(Slice);
      this->Betas[Slice]      = Other.Betas[Slice];
      this->Index[Slice]      = Other.Index[Slice];
      this->Adiabatic         = Other.Adiabatic;
      this->Coupling          = Other.Coupling;
  }


  ScalarType compute_overlap(SuperMode& Other, size_t &Slice)
  {
    return this->Fields.col(Slice).transpose() * Other.Fields.col(Slice);
  }

  ScalarType compute_overlap(SuperMode& Other, size_t &&Slice)
  {
    return this->Fields.col(Slice).transpose() * Other.Fields.col(Slice);
  }

  ScalarType compute_overlap(SuperMode& Other, size_t &&Slice0, size_t &&Slice1)
  {
    return this->Fields.col(Slice0).transpose() * Other.Fields.col(Slice1);
  }

  ScalarType compute_overlap(SuperMode& Other, size_t &Slice0, size_t &&Slice1)
  {
    return this->Fields.col(Slice0).transpose() * Other.Fields.col(Slice1);
  }


  ScalarType compute_coupling(SuperMode& Other, size_t Slice, VectorType &mesh_gradient, ScalarType &kInit)
  {
    ComplexScalarType C;
    if (this->mode_number == Other.mode_number)
    {
      C = 0.0;
    }

    else
    {
      VectorType overlap = this->Fields.col(Slice).cwiseProduct( Other.Fields.col(Slice) );

      ScalarType beta_0 = this->Betas[Slice], beta_1 = Other.Betas[Slice];

      C = - (ScalarType) 0.5 * J * kInit*kInit / sqrt(beta_0 *  beta_1) * abs( 1.0f / (beta_0 - beta_1) );

      ScalarType I = Trapz(overlap.cwiseProduct( mesh_gradient ), 1.0, Nx, Ny);

      C *= I;

      C = abs(C);
    }

    this->Coupling(Other.mode_number, Slice) = abs(C);
    Other.Coupling(this->mode_number, Slice) = abs(C);

    return abs(C);
  }


  ScalarType compute_adiabatic(SuperMode& Other, size_t Slice, VectorType &mesh_gradient, ScalarType &kInit)
  {
    ScalarType A;

    ScalarType beta_0 = this->Betas[Slice], beta_1 = Other.Betas[Slice];

    if (this->mode_number == Other.mode_number) { A = 0.0; }
    else { A = abs( (beta_0-beta_1) / compute_coupling(Other, Slice, mesh_gradient, kInit) ); }

    this->Adiabatic(Other.mode_number, Slice) = A;
    Other.Adiabatic(this->mode_number, Slice) = A;

    return A;
  }


  void populate_coupling_adiabatic(SuperMode& Other, size_t Slice, VectorType &mesh_gradient, ScalarType &kInit)
  {
    ComplexScalarType C;
    ScalarType A;

    ScalarType beta_0 = this->Betas[Slice], beta_1 = Other.Betas[Slice];

    if (this->mode_number == Other.mode_number)
    {
      C = 0.0;
      A = 0.0;
    }

    else
    {
      VectorType overlap = this->Fields.col(Slice).cwiseProduct( Other.Fields.col(Slice) );

      ScalarType beta_0 = this->Betas[Slice], beta_1 = Other.Betas[Slice];

      C  = - (ScalarType) 0.5 * J * kInit*kInit / sqrt(beta_0 *  beta_1) * abs( 1.0f / (beta_0 - beta_1) );

      ScalarType I = Trapz(overlap.cwiseProduct( mesh_gradient ), 1.0, Nx, Ny);

      C *=  I;

      C = abs(C);

      A = abs( (beta_0-beta_1) / C );
    }

    this->Coupling(Other.mode_number, Slice) = abs(C);
    Other.Coupling(this->mode_number, Slice) = abs(C);
    this->Adiabatic(Other.mode_number, Slice) = A;
    Other.Adiabatic(this->mode_number, Slice) = A;
  }


  ndarray get_fields(){ return eigen_to_ndarray_( this->Fields, { ITRLength, Ny, Nx} ); }
  ndarray get_index(){ return eigen_to_ndarray_( this->Index, { ITRLength} ); }
  ndarray get_betas(){ return eigen_to_ndarray_( this->Betas, { ITRLength} ); }
  ndarray get_adiabatic(){ return eigen_to_ndarray_( this->Adiabatic, { ITRLength, sMode} ); }

  ndarray get_coupling(){ return eigen_to_ndarray_( this->Coupling, { ITRLength, sMode} ); }
  ndarray get_adiabatic_specific(SuperMode& Mode){ return eigen_to_ndarray_( this->Adiabatic.row(Mode.mode_number), { ITRLength} ); }
  ndarray get_coupling_specific(SuperMode& Mode){ return eigen_to_ndarray_( this->Coupling.row(Mode.mode_number), { ITRLength} ); }
};



