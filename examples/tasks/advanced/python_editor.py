from pyface.toolkit import _toolkit_backend
backend = _toolkit_backend.strip(".").split(".")[-1]

if backend == "wx":
    from python_editor_wx import PythonEditor
elif backend == "qt4":
    from python_editor_qt4 import PythonEditor
else:
    raise RuntimeError("Unsupported toolkit %s" % backend)
