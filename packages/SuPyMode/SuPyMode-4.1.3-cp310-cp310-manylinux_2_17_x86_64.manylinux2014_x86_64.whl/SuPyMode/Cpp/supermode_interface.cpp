#include <pybind11/pybind11.h>
#include "includes/supermode.cpp"

PYBIND11_MODULE(SuperMode, module)
{
    module.doc() = "A c++ wrapper class for SuperMode";

    pybind11::class_<SuperMode>(module, "SuperMode")
    .def("get_fields",                &SuperMode::get_fields)
    .def("get_index",                 &SuperMode::get_index)
    .def("get_betas",                 &SuperMode::get_betas)
    .def("get_coupling",              &SuperMode::get_coupling)
    .def("get_adiabatic",             &SuperMode::get_adiabatic)
    .def("get_adiabatic_specific",    &SuperMode::get_adiabatic_specific)
    .def("get_coupling_specific",     &SuperMode::get_coupling_specific)
    .def_readwrite("left_boundary",   &SuperMode::left_boundary)
    .def_readwrite("right_boundary",  &SuperMode::right_boundary)
    .def_readwrite("top_boundary",    &SuperMode::top_boundary)
    .def_readwrite("bottom_boundary", &SuperMode::bottom_boundary)
    .def_readwrite("binding_number",  &SuperMode::mode_number);
}

