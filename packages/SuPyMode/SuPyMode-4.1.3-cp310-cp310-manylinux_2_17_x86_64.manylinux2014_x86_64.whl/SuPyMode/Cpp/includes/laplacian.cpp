#pragma once

#include "definitions.cpp"

class BaseLaplacian{
  public:
    std::string top_boundary, bottom_boundary, left_boundary, right_boundary;
    ndarray mesh;
    size_t n_x, n_y, size;
    ScalarType D0xy, D1y, D2y, D1x, D2x;
    MSparse Laplacian;
    bool Debug;
    Vecf2D finit_difference_matrix;

    BaseLaplacian(ndarray&  mesh){
      this->n_y = mesh.request().shape[0];
      this->n_x = mesh.request().shape[1];
      this->size = mesh.request().size;
      this->mesh = mesh;
      this->Laplacian = MSparse(this->size, this->size);
    }


    void FromTriplets()
    {
      Vecf1D Row  = finit_difference_matrix[0],
             Col  = finit_difference_matrix[1],
             Data = finit_difference_matrix[2];

      std::vector<fTriplet> Tri;
      Tri.reserve(Row.size());

      for (int i=0; i<Row.size(); i++)
          Tri.push_back(fTriplet(Col[i], Row[i], Data[i]));


       Laplacian.setFromTriplets(Tri.begin(), Tri.end());
    }


};
