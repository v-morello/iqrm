#include <pybind11/pybind11.h>

namespace py = pybind11;

double add(double a, double b) {
    return a + b;
}

PYBIND11_MODULE(libiqrm, m) {
    m.doc() = "libiqrm: C++ extensions for iqrm";
    m.def("add", &add, "Add two double-precision floats.", py::arg("a"), py::arg("b"));
}
