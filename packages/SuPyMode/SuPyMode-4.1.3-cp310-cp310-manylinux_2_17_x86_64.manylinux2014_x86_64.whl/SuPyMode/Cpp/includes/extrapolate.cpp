
#include "definitions.cpp"

std::vector<ScalarType> CoefD1 = {+1.0, -1.0};
std::vector<ScalarType> CoefD2 = {-1.0, 2.0, -1.0};
std::vector<ScalarType> CoefD3 = {+1.0, -3.0, 3.0, -1.0};


double
extrapolate_next_order_1_(std::vector<ScalarType>& y, std::vector<double>& x, size_t NextIter){
  return y[NextIter-1];
}


double
extrapolate_next_order_2_(std::vector<ScalarType>& y, std::vector<double>& x, size_t NextIter){
  double d1y = CoefD1[0] * y[NextIter-1] + CoefD1[1] * y[NextIter-2];
  return extrapolate_next_order_1_(y, x, NextIter) + d1y;
}


double
extrapolate_next_order_3_(std::vector<ScalarType>& y, std::vector<double>& x, size_t& NextIter){
  double d2y = CoefD2[0] * y[NextIter-1] + CoefD2[1] * y[NextIter-2] + CoefD2[2] * y[NextIter-3];
  return extrapolate_next_order_2_(y, x, NextIter) + d2y / 2.0;
}


double
extrapolate_next_order_4_(std::vector<ScalarType>& y, std::vector<double>& x, size_t& NextIter){
  double  d3y = CoefD3[0] * y[NextIter-1] + CoefD3[1] * y[NextIter-2] + CoefD3[2] * y[NextIter-3] + CoefD3[3] * y[NextIter-4];
  return extrapolate_next_order_3_(y, x, NextIter) + d3y / 6.0;
}




double
extrapolate_next(size_t order, std::vector<ScalarType>& y, std::vector<double>& x, size_t& NextIter)
{
  switch(order){

    case 1:
         return extrapolate_next_order_1_(y, x, NextIter);
         break;

    case 2:
         if ( NextIter < 2 )      { return extrapolate_next_order_1_(y, x, NextIter); }
         else                     { return extrapolate_next_order_2_(y, x, NextIter); }
         break;

    case 3:
         if      ( NextIter < 2 ) { return extrapolate_next_order_1_(y, x, NextIter); }
         else if ( NextIter < 3 ) { return extrapolate_next_order_2_(y, x, NextIter); }
         else                     { return extrapolate_next_order_3_(y, x, NextIter); }
         break;

    case 4:
         if      ( NextIter < 2 ) { return extrapolate_next_order_1_(y, x, NextIter); }
         else if ( NextIter < 3 ) { return extrapolate_next_order_2_(y, x, NextIter); }
         else if ( NextIter < 4 ) { return extrapolate_next_order_3_(y, x, NextIter); }
         else                     { return extrapolate_next_order_4_(y, x, NextIter); }
         break;

  };
  return 1;
}
