from pyface.toolkit import toolkit_object

if toolkit_object.toolkit == "wx":
    from python_editor_wx import PythonEditor
elif toolkit_object.toolkit == "qt4":
    from python_editor_qt4 import PythonEditor
else:
    raise RuntimeError("Unsupported toolkit %s" % toolkit_object.toolkit)
