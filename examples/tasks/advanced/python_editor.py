from pyface.toolkit import toolkit

if toolkit.toolkit == "wx":
    from python_editor_wx import PythonEditor
elif toolkit.toolkit == "qt4":
    from python_editor_qt4 import PythonEditor
else:
    raise RuntimeError("Unsupported toolkit %s" % toolkit.toolkit)
