%define DOCSTRING
"Classes for implementing a spreadsheet-like control, based on wxGrid"
%enddef

%module(package="wx", docstring=DOCSTRING) sheet

%{
#include <wx/sheet/sheet.h>

#include <iostream>

#include "wx/wxPython/wxPython.h"
#include "wx/wxPython/pyclasses.h"
%}

// import the wxPython interfaces
%import windows.i
%pythoncode { wx = _core }
%pythoncode { __docfilter__ = wx.__DocFilter(globals()) }

%include _sheet_rename.i

MAKE_CONST_WXSTRING_NOSWIG(EmptyString);
MAKE_CONST_WXSTRING_NOSWIG(PanelNameStr);
MAKE_CONST_WXSTRING_NOSWIG(DefaultDateTimeFormat);


//---------------------------------------------------------------------------
// Macros, similar to what's in helpers.h, to aid in the creation of
// virtual methods that are able to make callbacks to Python.  Many of these
// are specific to wxGrid and so are kept here to reduce the mess in helpers.h
// a bit.


%{
#define PYCALLBACK_GCA_COORDKIND(PCLASS, CBNAME)                               \
    wxSheetCellAttr CBNAME(wxSheetCoords coords, wxSheetAttr_Type c) {        \
        wxSheetCellAttr rval;                                            \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                            \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ro;                                                       \
            wxSheetCellAttr* ptr;                                                \
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(iii)", coords, c)); \
            if (ro) {                                                           \
                if (wxPyConvertSwigPtr(ro, (void **)&ptr, wxT("wxSheetCellAttr")))    \
                    rval = *ptr;                                                 \
                Py_DECREF(ro);                                                  \
            }                                                                   \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                             \
        if (! found)                                                            \
            return PCLASS::CBNAME(coords, c);                                     \
        return rval;                                                            \
    }                                                                           \
    wxSheetCellAttr base_##CBNAME(wxSheetCoords coords, wxSheetAttr_Type c) { \
        return PCLASS::CBNAME(coords, c);                                         \
    }



#define PYCALLBACK__GCACOORD(PCLASS, CBNAME)                                   \
    void CBNAME(wxSheetCoords coords, const wxSheetCellAttr& attr, wxSheetAttr_Type kind) {                           \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        bool found;                                                             \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iii)", coords, attr, kind));  \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            PCLASS::CBNAME(coords, attr, kind);                                         \
    }                                                                           \
    void base_##CBNAME(wxSheetCoords coords, const wxSheetCellAttr& attr, wxSheetAttr_Type kind) {                    \
        PCLASS::CBNAME(coords, attr, kind);                                             \
    }



#define PYCALLBACK__GCAINT(PCLASS, CBNAME)                                      \
    void CBNAME(wxSheetCellAttr *attr, int val) {                                \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        bool found;                                                             \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(ii)", attr, val));    \
            Py_DECREF(obj);                                                     \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                             \
        if (! found)                                                            \
            PCLASS::CBNAME(attr, val);                                          \
    }                                                                           \
    void base_##CBNAME(wxSheetCellAttr *attr, int val) {                         \
        PCLASS::CBNAME(attr, val);                                              \
    }



#define PYCALLBACK_INT__pure(CBNAME)                                            \
    int  CBNAME() {                                                             \
		std::cout << "PYCALLBACK_INT__pure " << m_myInst.m_self << "::" << #CBNAME << std::endl; \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        int rval = 0;                                                           \
        if (wxPyCBH_findCallback(m_myInst, #CBNAME))							\
        {																		\
			std::cout << "   found callback" << std::endl;                      \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("()"));         \
        }																		\
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }



#define PYCALLBACK_BOOL_COORD_pure(CBNAME)                                     \
    bool CBNAME(wxSheetCoords coords) {                                                 \
		std::cout << "PYCALLBACK_BOOL_COORD_pure #CBNAME" << std::endl; \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                            \
        bool rval = 0;                                                          \
        if (wxPyCBH_findCallback(m_myInst, #CBNAME))                            \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(ii)",coords));   \
        wxPyEndBlockThreads(blocked);                                             \
        return rval;                                                            \
    }


#define PYCALLBACK_STRING_COORD_pure(CBNAME)                                   \
    wxString CBNAME(wxSheetCoords coords) {                                             \
		std::cout << "PYCALLBACK_STRING_COORD_pure " << #CBNAME << std::endl; \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        wxString rval;                                                          \
        if (wxPyCBH_findCallback(m_myInst, #CBNAME)) {                          \
            PyObject* ro;                                                       \
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(ii)",coords));  \
            if (ro) {                                                           \
                rval = Py2wxString(ro);                                         \
                Py_DECREF(ro);                                                  \
            }                                                                   \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                                  \
        return rval;                                                            \
    }


#define PYCALLBACK__COORDSTRING_pure(CBNAME)                                   \
    void CBNAME(wxSheetCoords coords, const wxString& c) {                              \
		std::cout << "PYCALLBACK__COORDSTRING_pure " << #CBNAME << std::endl; \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        if (wxPyCBH_findCallback(m_myInst, #CBNAME)) {                          \
            PyObject* s = wx2PyString(c);                                       \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iiO)",coords,s));\
            Py_DECREF(s);                                                       \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                                  \
    }


#define PYCALLBACK_STRING_COORD(PCLASS, CBNAME)                                \
    wxString CBNAME(wxSheetCoords coords) {                                             \
		std::cout << "PYCALLBACK_STRING_COORD " << #CBNAME << std::endl; \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        wxString rval;                                                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ro;                                                       \
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(ii)",coords));  \
            if (ro) {                                                           \
                rval = Py2wxString(ro);                                         \
                Py_DECREF(ro);                                                  \
            }                                                                   \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(coords);                                        \
        return rval;                                                            \
    }                                                                           \
    wxString base_##CBNAME(wxSheetCoords coords) {                                      \
        return PCLASS::CBNAME(coords);                                            \
    }


#define PYCALLBACK_BOOL_COORDSTRING(PCLASS, CBNAME)                            \
    bool CBNAME(wxSheetCoords coords, const wxString& c)  {                             \
		std::cout << "PYCALLBACK_BOOL_COORDSTRING " << #CBNAME << std::endl; \
        bool rval = 0;                                                          \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* s = wx2PyString(c);                                       \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iiO)",coords,s));\
            Py_DECREF(s);                                                       \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(coords,c);                                       \
        return rval;                                                            \
    }                                                                           \
    bool base_##CBNAME(wxSheetCoords coords, const wxString& c) {                       \
        return PCLASS::CBNAME(coords,c);                                           \
    }




#define PYCALLBACK_LONG_COORD(PCLASS, CBNAME)                                  \
    long CBNAME(wxSheetCoords coords)  {                                                \
		std::cout << "PYCALLBACK_LONG_COORD " << #CBNAME << std::endl; \
        long rval;                                                              \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                            \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(ii)", coords));  \
        wxPyEndBlockThreads(blocked);                                             \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(coords);                                         \
        return rval;                                                            \
    }                                                                           \
    long base_##CBNAME(wxSheetCoords coords) {                                          \
        return PCLASS::CBNAME(coords);                                             \
    }



#define PYCALLBACK_BOOL_COORD(PCLASS, CBNAME)                                  \
    bool CBNAME(wxSheetCoords coords)  {                                                \
		std::cout << "PYCALLBACK_BOOL_COORD " << #CBNAME << std::endl; \
        bool rval = 0;                                                          \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                            \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(ii)", coords));  \
        wxPyEndBlockThreads(blocked);                                             \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(coords);                                         \
        return rval;                                                            \
    }                                                                           \
    bool base_##CBNAME(wxSheetCoords coords) {                                          \
        return PCLASS::CBNAME(coords);                                             \
    }



#define PYCALLBACK_DOUBLE_COORD(PCLASS, CBNAME)                                \
    double CBNAME(wxSheetCoords coords) {                                               \
		std::cout << "PYCALLBACK_DOUBLE_COORD " << #CBNAME << std::endl; \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                            \
        double rval;                                                            \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ro;                                                       \
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(ii)",coords));  \
            if (ro) {                                                           \
                PyObject* str = PyObject_Str(ro);                               \
                rval = PyFloat_AsDouble(str);                                   \
                Py_DECREF(ro);   Py_DECREF(str);                                \
            }                                                                   \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a, b);                                        \
        return rval;                                                            \
    }                                                                           \
    double base_##CBNAME(wxSheetCoords coords) {                                        \
        return PCLASS::CBNAME(a, b);                                            \
    }



#define PYCALLBACK__(PCLASS, CBNAME)                                            \
    void CBNAME()  {                                                            \
		std::cout << "PYCALLBACK__ " << #PCLASS << "::" << #CBNAME << std::endl; \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("()"));                \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            PCLASS::CBNAME();                                                   \
    }                                                                           \
    void base_##CBNAME() {                                                      \
        PCLASS::CBNAME();                                                       \
    }




#define PYCALLBACK_BOOL_SIZETSIZET(PCLASS, CBNAME)                              \
    bool CBNAME(size_t a, size_t b)  {                                          \
		std::cout << "PYCALLBACK_BOOL_SIZETSIZET " << #PCLASS << "::" << #CBNAME << std::endl; \
        bool rval = 0;                                                          \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(ii)", a,b));  \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(coords);                                         \
        return rval;                                                            \
    }                                                                           \
    bool base_##CBNAME(size_t a, size_t b) {                                    \
        return PCLASS::CBNAME(a,b);                                             \
    }



#define PYCALLBACK_BOOL_SIZET(PCLASS, CBNAME)                                   \
    bool CBNAME(size_t a)  {                                                    \
		std::cout << "PYCALLBACK_BOOL_SIZET " << #PCLASS << "::" << #CBNAME << std::endl; \
        bool rval = 0;                                                          \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(i)", a));     \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a);                                           \
        return rval;                                                            \
    }                                                                           \
    bool base_##CBNAME(size_t a) {                                              \
        return PCLASS::CBNAME(a);                                               \
    }


#define PYCALLBACK_STRING_INT(PCLASS, CBNAME)                                   \
    wxString CBNAME(int a) {                                                    \
		std::cout << "PYCALLBACK_STRING_INT " << #PCLASS << "::" << #CBNAME << std::endl; \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        wxString rval;                                                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ro;                                                       \
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(i)",a));     \
            if (ro) {                                                           \
                rval = Py2wxString(ro);                                         \
                Py_DECREF(ro);                                                  \
            }                                                                   \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a);                                           \
        return rval;                                                            \
    }                                                                           \
    wxString base_##CBNAME(int a) {                                             \
        return PCLASS::CBNAME(a);                                               \
    }


#define PYCALLBACK__INTSTRING(PCLASS, CBNAME)                                   \
    void CBNAME(int a, const wxString& c)  {                                    \
		std::cout << "PYCALLBACK__INTSTRING " << #PCLASS << "::" << #CBNAME << std::endl; \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* s = wx2PyString(c);                                       \
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iO)",a,s));          \
            Py_DECREF(s);                                                       \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            PCLASS::CBNAME(a,c);                                                \
    }                                                                           \
    void base_##CBNAME(int a, const wxString& c) {                              \
        PCLASS::CBNAME(a,c);                                                    \
    }




#define PYCALLBACK_BOOL_(PCLASS, CBNAME)                                        \
    bool CBNAME()  {                                                            \
		std::cout << "PYCALLBACK_BOOL_ " << #PCLASS << "::" << #CBNAME << std::endl; \
        bool rval = 0;                                                          \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("()"));         \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            rval = PCLASS::CBNAME();                                            \
        return rval;                                                            \
    }                                                                           \
    bool base_##CBNAME() {                                                      \
        return PCLASS::CBNAME();                                                \
    }



#define PYCALLBACK__SIZETINT(PCLASS, CBNAME)                                    \
    void CBNAME(size_t a, int b)  {                                             \
		std::cout << "PYCALLBACK__SIZETINT " << #PCLASS << "::" << #CBNAME << std::endl; \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(ii)", a,b));         \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            PCLASS::CBNAME(a,b);                                                \
    }                                                                           \
    void base_##CBNAME(size_t a, int b) {                                       \
        PCLASS::CBNAME(a,b);                                                    \
    }




#define PYCALLBACK__COORDLONG(PCLASS, CBNAME)                                  \
    void CBNAME(wxSheetCoords coords, long c)  {                                        \
		std::cout << "PYCALLBACK__COORDLONG " << #PCLASS << "::" << #CBNAME << std::endl; \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iii)", coords,c));      \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            PCLASS::CBNAME(coords,c);                                              \
    }                                                                           \
    void base_##CBNAME(wxSheetCoords coords, long c) {                                  \
        PCLASS::CBNAME(coords,c);                                                  \
    }




#define PYCALLBACK__COORDDOUBLE(PCLASS, CBNAME)                                \
    void CBNAME(wxSheetCoords coords, double c)  {                                      \
		std::cout << "PYCALLBACK__COORDDOUBLE " << #PCLASS << "::" << #CBNAME << std::endl; \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iif)", coords,c));      \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            PCLASS::CBNAME(coords,c);                                              \
    }                                                                           \
    void base_##CBNAME(wxSheetCoords coords, double c) {                                \
        PCLASS::CBNAME(coords,c);                                                  \
    }



#define PYCALLBACK__COORDBOOL(PCLASS, CBNAME)                                  \
    void CBNAME(wxSheetCoords coords, bool c)  {                                        \
		std::cout << "PYCALLBACK__COORDBOOL " << #PCLASS << "::" << #CBNAME << std::endl; \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                                                \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iii)", coords,c));      \
        wxPyEndBlockThreads(blocked);                                                  \
        if (! found)                                                            \
            PCLASS::CBNAME(a,b,c);                                              \
    }                                                                           \
    void base_##CBNAME(wxSheetCoords coords, bool c) {                                  \
        PCLASS::CBNAME(coords,c);                                                  \
    }




%}

//---------------------------------------------------------------------------
//---------------------------------------------------------------------------
//---------------------------------------------------------------------------

#define wxSHEET_VALUE_STRING     "string"
#define wxSHEET_VALUE_BOOL       "bool"
#define wxSHEET_VALUE_NUMBER     "long"
#define wxSHEET_VALUE_FLOAT      "double"
#define wxSHEET_VALUE_CHOICE     "choice"
#define wxSHEET_VALUE_TEXT       "string"
#define wxSHEET_VALUE_LONG       "long"
#define wxSHEET_VALUE_CHOICEINT  "choiceint"
#define wxSHEET_VALUE_DATETIME   "datetime"

enum wxSheetUpdate_Type
{
    wxSHEET_UpdateNone           = 0x0000, // update nothing
    
    wxSHEET_UpdateGridCellValues = 0x0001, // update the grid cell data container
    wxSHEET_UpdateRowLabelValues = 0x0002, // update the row label data container
    wxSHEET_UpdateColLabelValues = 0x0004, // update the col label data container
    wxSHEET_UpdateLabelValues    = wxSHEET_UpdateRowLabelValues|wxSHEET_UpdateColLabelValues, // update the label containers    
    wxSHEET_UpdateValues         = wxSHEET_UpdateGridCellValues|wxSHEET_UpdateLabelValues,
    
    wxSHEET_UpdateSpanned        = 0x0008, // update the spanned cells
    
    wxSHEET_UpdateGridCellAttrs  = 0x0010, // update grid cell attributes
    wxSHEET_UpdateRowLabelAttrs  = 0x0020, // update row label attributes
    wxSHEET_UpdateColLabelAttrs  = 0x0040, // update col label attributes
    wxSHEET_UpdateLabelAttrs     = wxSHEET_UpdateRowLabelAttrs|wxSHEET_UpdateColLabelAttrs,
    wxSHEET_UpdateAttributes     = wxSHEET_UpdateGridCellAttrs|wxSHEET_UpdateLabelAttrs, // update the attr container
    
    wxSHEET_UpdateSelection      = 0x0100, // update the selection
    
    wxSHEET_UpdateAll            = (wxSHEET_UpdateValues|wxSHEET_UpdateSpanned|wxSHEET_UpdateAttributes|wxSHEET_UpdateSelection),
    wxSHEET_UpdateType_Mask      = wxSHEET_UpdateAll
};

enum wxSheetSelectionMode_Type 
{
	wxSHEET_SelectNone  = 0x0001, // don't allow selections by mouse or keyboard
								// direct calls to the selections work however
	wxSHEET_SelectCells = 0x0002, // single cells, blocks, rows, and cols
	wxSHEET_SelectRows  = 0x0004, // only rows can be selected
	wxSHEET_SelectCols  = 0x0008  // only cols can be selected
};
%pythoncode {
SelectNone    = wxSHEET_SelectNone;
SelectCells   = wxSHEET_SelectCells
SelectRows    = wxSHEET_SelectRows
SelectColumns = wxSHEET_SelectCols
}

enum wxSheetAttr_Type    
{
    wxSHEET_AttrDefault = 0x00010, 
    wxSHEET_AttrCell    = 0x00020, 
    wxSHEET_AttrRow     = 0x00040, 
    wxSHEET_AttrCol     = 0x00080, 
    wxSHEET_AttrAny     = wxSHEET_AttrDefault|wxSHEET_AttrCell|wxSHEET_AttrRow|wxSHEET_AttrCol,    
    wxSHEET_AttrType_Mask = wxSHEET_AttrAny
};



%typemap(out) wxArraySheetBlock& {
    $result = PyList_New(0);
    size_t idx;
    for (idx = 0; idx < (*$1).GetCount(); idx += 1) {
        wxSheetBlock& block = (*$1).Item(idx);
        PyObject* obj = SWIG_NewPointerObj((void *)(&block), SWIGTYPE_p_wxSheetBlock, 0);
        PyList_Append($result, obj);
        Py_DECREF(obj);
    }
}

%typemap(out) wxPoint {
	$result = PyTuple_New(2);
    PyTuple_SET_ITEM($result, 0, PyInt_FromLong($1.x));
    PyTuple_SET_ITEM($result, 1, PyInt_FromLong($1.y));
}	
	
class wxSheetCoords
{
public:
    wxSheetCoords();
    wxSheetCoords( int row, int col );
    
    int  GetRow() const;
    int  GetCol() const;

    void SetRow( int row );
    void SetCol( int col );
    void Set( int row, int col );

    wxSheetCoords& ShiftRow( int row );
    wxSheetCoords& ShiftCol( int col );
    wxSheetCoords& Shift( int rows, int cols );
    void SwapRowCol();

    wxSheetCoords GetShifted( int rows, int cols ) const;
    wxSheetCoords GetSwapped() const;

    wxSheetCoords SheetToRowLabel()    const;
    wxSheetCoords SheetToColLabel()    const;
    wxSheetCoords SheetToCornerLabel() const;
    
    bool UpdateRows( size_t row, int numRows );
    bool UpdateCols( size_t col, int numCols );
    
    wxSheetCoords operator+(const wxSheetCoords& c);
    wxSheetCoords operator-(const wxSheetCoords& c);
    wxSheetCoords& operator+=(const wxSheetCoords& c);
    wxSheetCoords& operator-=(const wxSheetCoords& c);
    bool operator == (const wxSheetCoords& other) const;
    bool operator != (const wxSheetCoords& other) const;
    bool operator <  (const wxSheetCoords& other) const;
    bool operator <= (const wxSheetCoords& other) const;
    bool operator >  (const wxSheetCoords& other) const;
    bool operator >= (const wxSheetCoords& other) const;

    int m_row;
    int m_col;    
};
	

class wxSheetChildWindow : public wxWindow
{
public:
    wxSheetChildWindow( wxSheet *parent, wxWindowID id = wxID_ANY,
                        const wxPoint &pos = wxDefaultPosition, 
                        const wxSize &size = wxDefaultSize,
                        long style = wxWANTS_CHARS|wxBORDER_NONE|wxCLIP_CHILDREN,
                        const wxString& name = wxT("wxSheetChildWindow") );

    // implementation
    void OnPaint( wxPaintEvent& event );
    void OnMouse( wxMouseEvent& event );
    void OnKeyAndChar( wxKeyEvent& event );
    void OnFocus( wxFocusEvent& event );
    void OnEraseBackground( wxEraseEvent& ); 

    wxSheet* GetOwner() const { return m_owner; }
    
    wxSheet *m_owner;
    int      m_mouseCursor; // remember the last cursor set for this window  
    
    %extend {
		wxWindow* CastAsWxWindow()
		{
			return static_cast<wxWindow*>(self);
		}
	}
      
};

/*
class wxSheetRefData : public wxObjectRefData
{
public:
    wxSheetRefData();
    virtual ~wxSheetRefData();\
    
    // Find/Add/Remove sheets that share this data - used for wxSheetSplitter
    int  FindSheet(wxSheet* sheet) const;
    bool HasSheet(wxSheet* sheet) const;
    void AddSheet(wxSheet* sheet);
    void RemoveSheet(wxSheet* sheet);
    wxSheet *GetSheet(size_t n) const;
    size_t GetSheetCount() const;

};
*/

MustHaveApp(wxSheet);

class wxSheet : public wxWindow
{
public:
    wxSheet( wxWindow *parent, wxWindowID id,
             const wxPoint& pos = wxDefaultPosition,
             const wxSize& size = wxDefaultSize,
             long style = wxWANTS_CHARS,
             const wxString& name = wxT("wxSheet") );

    bool Create( wxWindow *parent, wxWindowID id,
                 const wxPoint& pos = wxDefaultPosition,
                 const wxSize& size = wxDefaultSize,
                 long style = wxWANTS_CHARS,
                 const wxString& name = wxT("wxSheet") );                 

    virtual ~wxSheet();
    virtual bool Destroy();    

    // ref another wxSheet's ref data - see usage in wxSheetSplitter
    void RefSheet(wxSheet* otherSheet);
    // Create a new wxSheet with same parent, used for wxSheetSplitter.
    //   override this so that the top left sheet in the splitter can return
    //   a "new MySheet" for the other sheets as necessary
    //   This is one of the few ways for the splitter to create new sheets.
    virtual wxSheet* Clone(wxWindowID id = wxID_ANY);

    // override wxWindow::Enable to ensure proper refresh
    virtual bool Enable(bool enable = true);

    // ------------------------------------------------------------------------
    // Create/Set/Get wxSheetTable - the underlying data to be displayed

    wxSheetTable* GetTable() const { return GetSheetRefData()->m_table; }
    // Set your own table derived from wxSheetTable, if takeOwnership the
    //   the table will be deleted when this window is destroyed
    bool SetTable( wxSheetTable *table, bool takeOwnership );  
    
    // Create a wxSheetTable using string data containers to use
    //   see this function to see how to setup the table and use SetTable 
    //   for the case where you want to customize things
    //   This function exists to show how to  create and assign tables
    bool CreateGrid( int numRows, int numCols, int options = 0 );

    // ------------------------------------------------------------------------
    // Dimensions of the number of cells on the sheet and helper cell functions
    
    int GetNumberRows() const { return GetSheetRefData()->m_rowEdges.GetCount(); }
    int GetNumberCols() const { return GetSheetRefData()->m_colEdges.GetCount(); }

    // Is the coords anywhere in labels or grid, -1 to GetNumberRows/Cols()-1
    bool ContainsCell( const wxSheetCoords& coords ) const 
        { return (coords.m_row >= -1) && (coords.m_col >= -1) &&
                 (coords.m_row < GetNumberRows()) && 
                 (coords.m_col < GetNumberCols()); }
                 
    // returns true if the coords are within the grid cells of the sheet
    bool ContainsGridRow( int row ) const { return (row >= 0) && (row < GetNumberRows()); }
    bool ContainsGridCol( int col ) const { return (col >= 0) && (col < GetNumberCols()); }
    bool ContainsGridCell( const wxSheetCoords& coords ) const
        { return ContainsGridRow(coords.m_row) && ContainsGridCol(coords.m_col); }

    // returns true if the coords are within the row/col label cells
    bool ContainsRowLabelCell( const wxSheetCoords& coords ) const
        { return (coords.m_col == -1) && ContainsGridRow(coords.m_row); }
    bool ContainsColLabelCell( const wxSheetCoords& coords ) const
        { return (coords.m_row == -1) && ContainsGridCol(coords.m_col); }

    // static helper functions to determine what type of cell it is, not check validity
        
    static bool IsGridCell(const wxSheetCoords& coords);
    static bool IsLabelCell(const wxSheetCoords& coords);
    static bool IsRowLabelCell(const wxSheetCoords& coords);
    static bool IsColLabelCell(const wxSheetCoords& coords);
    static bool IsCornerLabelCell(const wxSheetCoords& coords);
    
    // Get an enum value of what window the coords are meant for
//    static wxSheetCell_Type GetCellCoordsType(const wxSheetCoords& coords);
        
    // "clear" the contents of the grid (depends on table's Clear() function)
    //   the string implementations clear the cell values, not the # rows/cols
    void ClearValues(int update = wxSHEET_UpdateValues); 
        
    // Insert/Add/DeleteRows/Cols to the grid cells
    //   update contains or'ed values of enum wxSheetUpdate_Type.
    //   you proabably want UpdateAll unless you ensure that no problems will occur
    //   or you will update some other way
    bool InsertRows( size_t row, size_t numRows, int update = wxSHEET_UpdateAll );
    bool AppendRows( size_t numRows, int update = wxSHEET_UpdateAll );
    bool DeleteRows( size_t row, size_t numRows, int update = wxSHEET_UpdateAll );
        
    bool InsertCols( size_t col, size_t numCols, int update = wxSHEET_UpdateAll );
    bool AppendCols( size_t numCols, int update = wxSHEET_UpdateAll );
    bool DeleteCols( size_t col, size_t numCols, int update = wxSHEET_UpdateAll );

    // Set exactly the number of rows or cols, these functions Append or
    // Delete rows/cols to/from the end. If you are setting attributes for 
    // particular cells/rows/cols you probably won't want to use these
    bool SetNumberRows( size_t rows, int update = wxSHEET_UpdateAll );
    bool SetNumberCols( size_t cols, int update = wxSHEET_UpdateAll );
    bool SetNumberCells( size_t rows, size_t cols, int update = wxSHEET_UpdateAll );
    
    // Inserting/Appending/Deleting rows/cols functions are forwarded here
    //   and then sent to the wxSheetTable::UpdateRows/Cols functions.
    //   numRows/Cols > 0 : InsertRows/Cols at row/col else if < 0 delete
    //   row/col == GetNumberRows/Cols && numRows/Cols > 0 to append to end
    virtual bool UpdateRows( size_t row, int numRows, int update = wxSHEET_UpdateAll );
    virtual bool UpdateCols( size_t col, int numCols, int update = wxSHEET_UpdateAll );
        
    // ------------------------------------------------------------------------
    // Dimensions of the row and column sizes
    
    // Get/Set the default height/width of newly created rows/cols
    //   if resizeExisting then resize all to match the newly set default
    int  GetDefaultRowHeight() const { return GetSheetRefData()->m_rowEdges.GetDefaultSize(); }
    int  GetDefaultColWidth()  const { return GetSheetRefData()->m_colEdges.GetDefaultSize(); }
    void SetDefaultRowHeight( int height, bool resizeExistingRows = false );
    void SetDefaultColWidth( int width, bool resizeExistingCols = false );
    
    // Get/Set the absolute min row/col width/height, 0 for no min size
    //   Call during grid creation, existing rows/cols are not resized
    //   This value is used when dragging cell size with the mouse if no 
    //   particular min size for a row/col has been set
    int  GetMinimalAcceptableRowHeight() const { return GetSheetRefData()->m_rowEdges.GetMinAllowedSize(); }
    int  GetMinimalAcceptableColWidth()  const { return GetSheetRefData()->m_colEdges.GetMinAllowedSize(); }
    void SetMinimalAcceptableRowHeight(int height) { GetSheetRefData()->m_rowEdges.SetMinAllowedSize(height); }
    void SetMinimalAcceptableColWidth(int width)   { GetSheetRefData()->m_colEdges.SetMinAllowedSize(width); }

    // Don't allow specific rows/cols to be resized smaller than this
    //   Call during grid creation, existing rows/cols are not resized
    //   The setting is cleared to default val if width/height is < min acceptable
    int  GetMinimalRowHeight(int row) const { return GetSheetRefData()->m_rowEdges.GetMinSize(row); }
    int  GetMinimalColWidth(int col) const  { return GetSheetRefData()->m_colEdges.GetMinSize(col); }
    void SetMinimalRowHeight(int row, int height) { GetSheetRefData()->m_rowEdges.SetMinSize(row, height); }
    void SetMinimalColWidth(int col, int width)   { GetSheetRefData()->m_colEdges.SetMinSize(col, width); }

    // Set the height of a row or width of a col, -1 notation for labels
    //  use height/width = -1 to autosize from the row/col labels
    void SetRowHeight( int row, int height );
    void SetColWidth(  int col, int width );
    
    // Get the height/top/bottom for rows, uses -1 notation
    int GetRowHeight(int row) const;
    int GetRowTop(int row) const;
    int GetRowBottom(int row) const;
    // Get the width/left/right for cols, uses -1 notation
    int GetColWidth(int col) const;
    int GetColLeft(int col) const;
    int GetColRight(int col) const;
    // Get the width, height of a cell as a wxSize, -1 notation
    //  this does not include spanned cells
    wxSize GetCellSize(const wxSheetCoords& coords) const;
        
    // does the cell have a non-zero width and height, may not be visible, -1 notation
    bool IsCellShown( const wxSheetCoords& coords ) const;
       
    // grid may occupy more space than needed for its rows/columns, this
    // function allows to set how big this margin space is
    void SetMargins(int width, int height)
        { GetSheetRefData()->m_marginSize.x = wxMax(0, width); 
          GetSheetRefData()->m_marginSize.y = wxMax(0, height); }
    
    // Get the renderer's best size for the cell, uses -1 notation
    wxSize GetCellBestSize(const wxSheetCoords& coords, wxDC *dc = NULL) const;
    // Get the best height of a row or the best width of a col using the 
    //   renderer's best size, iterating though all cells in the row or col.
    int GetRowBestHeight(int row) const;
    int GetColBestWidth(int col) const;

    // ------------------------------------------------------------------------
    // Row/Col label size

    // Get the fixed initial size of the width of row labels or height of col labels
    int GetDefaultRowLabelWidth()  const { return WXSHEET_DEFAULT_ROW_LABEL_WIDTH; }
    int GetDefaultColLabelHeight() const { return WXSHEET_DEFAULT_COL_LABEL_HEIGHT; }

    // Get/Set the row/col label widths, 
    //   if zero_not_shown and row/col & corner not shown return 0
    int  GetRowLabelWidth(bool zero_not_shown = true)  const;
    int  GetColLabelHeight(bool zero_not_shown = true) const;
    void SetRowLabelWidth( int width );
    void SetColLabelHeight( int height );

    // ------------------------------------------------------------------------
    // Auto sizing of the row/col widths/heights
    
    // automatically size the col/row to fit to its contents, if setAsMin, 
    // this optimal width will also be set as minimal width for this column
    // returns the width or height used.
    int AutoSizeRow( int row, bool setAsMin = true );
    int AutoSizeCol( int col, bool setAsMin = true );

    // auto size all columns (very ineffective for big grids!)
    void AutoSizeRows( bool setAsMin = true );
    void AutoSizeCols( bool setAsMin = true );

    // auto size the grid, that is make the columns/rows of the "right" size
    // and also set the grid size to just fit its contents
    void AutoSize( bool setAsMin = true );

    // autosize row height depending on label text
    void AutoSizeRowLabelHeight( int row );
    // autosize column width depending on label text
    void AutoSizeColLabelWidth( int col );

    // Force the col widths to be of equal size so that they fit within the 
    // the window size. This is maintained even when the window is resized. 
    // The col widths will not be sized less than min_width in pixels. 
    // Use this if you know that the window will be of a reasonable size to 
    // fit the cols, but you don't want to track the EVT_SIZE yourself.
    // use a min_width = 0 to turn it off
    void SetEqualColWidths(int min_width);
    
    // ------------------------------------------------------------------------
    // Row/Col drag resizing enabled or disabled
    //
    // if CanDragRow/ColSize the rows/cols can be resized by the mouse
    // if CanDragGridSize you can resize the rows/cols in the grid window
    //   else you resize in the label windows (if CanDragRow/ColSize is true)
    
    void EnableDragRowSize( bool enable = true );
    void EnableDragColSize( bool enable = true );
    void EnableDragGridSize(bool enable = true );
    void DisableDragRowSize();
    void DisableDragColSize();
    void DisableDragGridSize();
    bool CanDragRowSize()  const;
    bool CanDragColSize()  const;
    bool CanDragGridSize() const;
    
    // Directly set the dragging of the cell size use wxSheetDragCellSize_Type enums
    void SetDragCellSize( int type );
    void SetDragCellSize( int type, bool enable );
    int GetDragCellSize() const;
    
    // ------------------------------------------------------------------------
    // Grid line, cell highlight, selection colouring

    // Draw the grid lines, wxHORIZONAL | wxVERTICAL (wxBOTH), 0 for none
    void EnableGridLines( int dir = wxBOTH );
    int  GridLinesEnabled() const;
    
    const wxColour& GetGridLineColour() const;
    void            SetGridLineColour( const wxColour& colour );
    
    const wxColour& GetCursorCellHighlightColour();
    int             GetCursorCellHighlightPenWidth()   const;
    int             GetCursorCellHighlightROPenWidth() const;
    void            SetCursorCellHighlightColour( const wxColour& colour );
    void            SetCursorCellHighlightPenWidth(int width);
    void            SetCursorCellHighlightROPenWidth(int width);

    // get/set the colour bounding the labels to give 3-D effect
    const wxColour& GetLabelOutlineColour() const;
    void            SetLabelOutlineColour( const wxColour& colour );
    
    const wxColour& GetSelectionBackground() const;
    const wxColour& GetSelectionForeground() const;
    void            SetSelectionBackground(const wxColour& c);
    void            SetSelectionForeground(const wxColour& c);
    
    // ------------------------------------------------------------------------
    // Span, cells can span across multiple cells, hiding cells below
    //
    // Normally cells are of size 1x1, but they can be larger. 
    // The other cells can still have values and attributes, but they
    // will not be used since GetCellOwner is used for most coord operations
    // so that the underlying cell values and attributes are ignored.
    // The span for the owner cell is 1x1 or larger, the span for other
    // cells contained within the spanned block have a cell span of <= 0, such 
    // that coords + GetCellSpan() = the owner cell
    //
    // You can completely override this functionality if you provide 
    //   HasSpannedCells, GetCellBlock, SetCellSpan

    // Are there any spanned cells at all?
    virtual bool HasSpannedCells() const;
    
    // if cell is part of a spanning cell, return owner's coords else input coords
    wxSheetCoords GetCellOwner( const wxSheetCoords& coords ) const;    
    // Get a block of the cell, unless a spanned cell it's of size 1,1
    //   note: the top left of block is the owner cell of coords
    virtual wxSheetBlock GetCellBlock( const wxSheetCoords& coords ) const;
    // Get the span of a cell, the owner (top right) cell always has a span of 
    //  (1, 1) or greater. The other cells in a spanned block will have a span 
    //  (<1, <1) such that, coords + coordsSpan = ownerCoords
    wxSheetCoords GetCellSpan( const wxSheetCoords& coords ) const;
    // Set the span of a cell, must be 1x1 or greater, 
    // To remove a spanned cell set it to a cell of size 1x1
    // For grid cells the whole block must be contained within the grid cells 
    //  and if the block intersects a previously spanned cell block the top left 
    //  corners must match up. 
    // Row and Col labels can span cells as well, spanned row labels must have a
    //  width of 1 and a height of >= 1, col labels a height of 1 and width >= 1
    virtual void SetCellSpan( const wxSheetBlock& block );
    void SetCellSpan( const wxSheetCoords& coords, const wxSheetCoords& numRowsCols );

    // Get a pointer to the spanned blocks to iterate through, may return NULL.
    const wxSheetSelection* GetSpannedBlocks() const;
    
    // ------------------------------------------------------------------------
    // Get/Set attributes for the cells, row, col, corner labels

    // See wxSheetAttr_Type for a description of the type of attribute

    // The coords are specified as
    //   Grid area    : (0 <= row < GetNumberRows), (0 <= col < GetNumberCols)
    //   Corner label : row = col = -1
    //   Row labels   : (0 <= row < GetNumberRows), col = -1
    //   Col labels   : row = -1, (0 <= col < GetNumberCols)
    
    // For the wxSHEET_AttrDefault type the coords should be contained within the 
    //   size of the sheet, but the particular values are not used.
    //   see const wxGridCellSheetCoords = (0,0) for example
    //   wxRowLabelSheetCoords, wxColLabelSheetCoords, wxCornerLabelSheetCoords
    
    // To completely override this you may provide alternate 
    // GetOrCreateAttr, GetAttr, and SetAttr functions.  

    // Make sure that the last default attr of initAttr is defAttr
    //   This is called internally when you call SetAttr and should not be
    //   needed unless you want to specially chain together attributes.
    bool InitAttr( wxSheetCellAttr& initAttr, const wxSheetCellAttr& defAttr ) const;

    // Get an attribute for the coords if it exists or create a new one 
    // and put it into the table which puts it in the attr provider.
    // The type may be only be wxSHEET_AttrDefault/Cell/Row/Col for the grid cells
    // and wxSHEET_AttrDefault/Cell for the labels
    virtual wxSheetCellAttr GetOrCreateAttr( const wxSheetCoords& coords, 
                                             wxSheetAttr_Type type ) const;
 
    // Get the attribute for any area depending on the coords and type
    // returns a valid attr if the coords are valid and type = wxSHEET_AttrAny
    // The type may be only be wxSHEET_AttrDefault/Cell/Row/Col/Any for the grid cells
    // and wxSHEET_AttrDefault/Cell/Any for the labels
    virtual wxSheetCellAttr GetAttr( const wxSheetCoords& coords, 
                                     wxSheetAttr_Type type = wxSHEET_AttrAny) const;
    // Set the attribute for any area depending on the coords
    // The type may be only be wxSHEET_AttrDefault/Cell/Row/Col for the grid cells
    // and wxSHEET_AttrDefault/Cell for the labels
    virtual void SetAttr(const wxSheetCoords& coords, const wxSheetCellAttr& attr,
                         wxSheetAttr_Type type );

    // ------ Simplified functions for accessing the attributes ---------------
    // Get an attribute for the grid coords, returning a cell/row/col attr or
    //   if multiple attr for the coords an attr that's merged, or the def attr
    wxSheetCellAttr GetGridAttr(const wxSheetCoords& coords) const;

    // Get a specific Cell/Row/Col attr for the coords in the grid
    //   if none set returns wxNullSheetCellAttr
    wxSheetCellAttr GetGridCellAttr(const wxSheetCoords& coords) const;
    wxSheetCellAttr GetGridRowAttr(int row) const;
    wxSheetCellAttr GetGridColAttr(int col) const;
    // Set a specific Cell/Row/Col attr for coords, row/col only apply to the grid
    void SetGridCellAttr(const wxSheetCoords& coords, const wxSheetCellAttr& attr);
    void SetGridRowAttr(int row, const wxSheetCellAttr& attr);
    void SetGridColAttr(int col, const wxSheetCellAttr& attr);

    // Get the row/col/corner label attributes, if one is not set for the 
    //  particular coords, returns the default one. (note: only one corner attr)
    //  if you want the particular attr use GetRow/ColLabelCellAttr
    wxSheetCellAttr GetRowLabelAttr(int row) const;
    wxSheetCellAttr GetColLabelAttr(int col) const;
    wxSheetCellAttr GetCornerLabelAttr() const;

    // Get a specific attr the row/col/corner label cell
    //   if none set returns wxNullSheetCellAttr
    wxSheetCellAttr GetRowLabelCellAttr(int row) const;
    wxSheetCellAttr GetColLabelCellAttr(int col) const;
    // Set a specific attribute for particular row/col/corner label cell
    void SetRowLabelCellAttr(int row, const wxSheetCellAttr& attr);
    void SetColLabelCellAttr(int col, const wxSheetCellAttr& attr);
    void SetCornerLabelAttr(const wxSheetCellAttr& attr);
   
    // Get/Set default attributes for the areas (only one corner attr)
    //  For setting, wxSheetCellAttr::UpdateWith is called with the current default 
    //  attr so you so need only set the values that you want to change.
    wxSheetCellAttr GetDefaultAttr(const wxSheetCoords& coords) const;
    wxSheetCellAttr GetDefaultGridCellAttr() const;
    wxSheetCellAttr GetDefaultRowLabelAttr() const;
    wxSheetCellAttr GetDefaultColLabelAttr() const;
    void SetDefaultAttr(const wxSheetCoords& coords, const wxSheetCellAttr& attr);
    void SetDefaultGridCellAttr(const wxSheetCellAttr& attr);
    void SetDefaultRowLabelAttr(const wxSheetCellAttr& attr);
    void SetDefaultColLabelAttr(const wxSheetCellAttr& attr);
    
    // These are convienience functions, if for example you want to subclass the
    //  table and modify and return default attr "on the fly" for each cell.
    //  Please use the standard methods if at all possible.
    const wxSheetCellAttr& DoGetDefaultGridAttr() const;
    const wxSheetCellAttr& DoGetDefaultRowLabelAttr() const;
    const wxSheetCellAttr& DoGetDefaultColLabelAttr() const;
    const wxSheetCellAttr& DoGetDefaultCornerLabelAttr() const;
    
    // Get/Set particular attributes for any type of cell/row/col anywhere
    //  The default is to get the attr val for type=wxSHEET_AttrAny meaning that
    //  it'll find a set attr first or return the default attr value as a last resort. 
    //  For GetXXX you will receive an an error message if you specify a 
    //  particular wxSHEET_AttrCell/Row/Col, but there isn't an attribute set
    const wxColour& GetAttrBackgroundColour( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    const wxColour& GetAttrForegoundColour( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    const wxFont&   GetAttrFont( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    int             GetAttrAlignment( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    int             GetAttrOrientation( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    int             GetAttrLevel( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    bool            GetAttrOverflow( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    bool            GetAttrOverflowMarker( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    bool            GetAttrShowEditor( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    bool            GetAttrReadOnly( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    wxSheetCellRenderer GetAttrRenderer( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    wxSheetCellEditor   GetAttrEditor( const wxSheetCoords& coords, wxSheetAttr_Type type = wxSHEET_AttrAny ) const;
    
    // Set attributes for a particular cell/row/col, relies on GetOrCreateAttr()
    //  so it creates and adds the attr to the attr provider if there wasn't one
    //  after setting the particular value.
    //  The type may be only be wxSHEET_AttrDefault/Cell/Row/Col 
    void SetAttrBackgroundColour( const wxSheetCoords& coords, const wxColour& colour, wxSheetAttr_Type type = wxSHEET_AttrCell );
    void SetAttrForegroundColour( const wxSheetCoords& coords, const wxColour& colour, wxSheetAttr_Type type = wxSHEET_AttrCell );
    void SetAttrFont( const wxSheetCoords& coords, const wxFont& font, wxSheetAttr_Type type = wxSHEET_AttrCell );
    void SetAttrAlignment( const wxSheetCoords& coords, int align, wxSheetAttr_Type type = wxSHEET_AttrCell );
    void SetAttrOrientation( const wxSheetCoords& coords, int orientation, wxSheetAttr_Type type = wxSHEET_AttrCell );
    void SetAttrLevel( const wxSheetCoords& coords, int level, wxSheetAttr_Type type = wxSHEET_AttrCell );
    void SetAttrOverflow( const wxSheetCoords& coords, bool allow, wxSheetAttr_Type type = wxSHEET_AttrCell );
    void SetAttrOverflowMarker( const wxSheetCoords& coords, bool draw_marker, wxSheetAttr_Type type = wxSHEET_AttrCell );
    void SetAttrShowEditor( const wxSheetCoords& coords, bool show_editor, wxSheetAttr_Type type = wxSHEET_AttrCell );
    void SetAttrReadOnly( const wxSheetCoords& coords, bool isReadOnly, wxSheetAttr_Type type = wxSHEET_AttrCell );
    void SetAttrRenderer( const wxSheetCoords& coords, const wxSheetCellRenderer &renderer, wxSheetAttr_Type type = wxSHEET_AttrCell );
    void SetAttrEditor( const wxSheetCoords& coords, const wxSheetCellEditor &editor, wxSheetAttr_Type type = wxSHEET_AttrCell );

    // helper functions that use SetColAttr to set renderer type
    // set the format for the data in the column: default is string
    void SetColFormatBool(int col);
    void SetColFormatNumber(int col);
    void SetColFormatFloat(int col, int width = -1, int precision = -1);
    void SetColFormatCustom(int col, const wxString& typeName);

    // ------------------------------------------------------------------------
    // Get/Set cell, row, col, and corner label values
    // To completely override this you need only provide Get/SetCellValue
    
    // Get/Set cell value, uses coords = -1 notation for row/col/corner labels
    virtual wxString GetCellValue( const wxSheetCoords& coords );
    virtual void SetCellValue( const wxSheetCoords& coords, const wxString& value );
    
    // Is this cell empty, see wxSheetTable
    virtual bool HasCellValue( const wxSheetCoords& coords );
    
    wxString GetRowLabelValue( int row );
    wxString GetColLabelValue( int col );
    void     SetRowLabelValue( int row, const wxString& value );
    void     SetColLabelValue( int col, const wxString& value );

    wxString GetCornerLabelValue();
    void     SetCornerLabelValue(const wxString& value);
    
    // ------------------------------------------------------------------------
    // Register mapping between data types to Renderers/Editors

    // I don't fully understand the reasoning for these, it's some sort of 
    //  string registry for the editors and renderers. 
    //  It's not clear to me why this is useful. - John Labenski

    void RegisterDataType( const wxString& typeName,
                           const wxSheetCellRenderer& renderer,
                           const wxSheetCellEditor& editor );

    virtual wxSheetCellEditor   GetDefaultEditorForType(const wxString& typeName) const;
    virtual wxSheetCellRenderer GetDefaultRendererForType(const wxString& typeName) const;
    
    // FIXME what is the point of these?
    virtual wxSheetCellEditor   GetDefaultEditorForCell(const wxSheetCoords& coords) const;
    virtual wxSheetCellRenderer GetDefaultRendererForCell(const wxSheetCoords& coords) const;

    // ------------------------------------------------------------------------
    // Cursor movement and visibility functions

    // Check to see if a cell is either wholly visible (the default arg)
    //   or at least partially visible, uses -1 notation for labels
    bool IsCellVisible( const wxSheetCoords& coords, bool wholeCellVisible = true ) const;
    bool IsRowVisible( int row, bool wholeRowVisible = true ) const;
    bool IsColVisible( int col, bool wholeColVisible = true ) const;
    // Make this cell visible, uses -1 notation, will not unhide label windows
    void MakeCellVisible( const wxSheetCoords& coords );

    // Get/Set cursor cell, this is the "current" cell where a highlight is drawn.
    //  The cursor only applies to the grid cells.
    const wxSheetCoords& GetGridCursorCell() const;
    int  GetGridCursorRow() const;
    int  GetGridCursorCol() const;
    void SetGridCursorCell( const wxSheetCoords& coords );
    
    // These are simplified methods for moving the cursor, mostly used internally
    //  for handling key press movements.
    bool MoveCursorUp( bool expandSelection );
    bool MoveCursorDown( bool expandSelection );
    bool MoveCursorLeft( bool expandSelection );
    bool MoveCursorRight( bool expandSelection );
    bool MoveCursorUpBlock( bool expandSelection );
    bool MoveCursorDownBlock( bool expandSelection );
    bool MoveCursorLeftBlock( bool expandSelection );
    bool MoveCursorRightBlock( bool expandSelection );
    bool MoveCursorUpPage( bool expandSelection );
    bool MoveCursorDownPage( bool expandSelection );

    virtual bool DoMoveCursor( const wxSheetCoords& relCoords, bool expandSelection ); 
    virtual bool DoMoveCursorBlock( const wxSheetCoords& relDir, bool expandSelection );
    virtual bool DoMoveCursorUpDownPage( bool page_up, bool expandSelection );
    
    // ------------------------------------------------------------------------
    // Cell/Row/Col selection and deselection, you can only select grid cells.

    // Note: A selection to the # of rows/cols means that the whole row/col is
    //   selected. Otherwise the right/bottom is rows/cols - 1, ie. contained
    //   within the actual number of cells.
    //   If sendEvt a wxEVT_SHEET_RANGE_SELECTED is sent, the SELECTING event
    //     should have been sent by the caller and if vetoed not call these.
    //   All functions (De)Select/Row/Col/Cell, SelectAll go to (De)SelectBlock.
    //   ClearSelection deselects everything and sends a single event with
    //   wxSheetBlock(0,0,rows,cols) to imply everything is cleared.
    
    // To override the selection mechanism you only need to override,
    // HasSelection, IsBlockSelected, SelectBlock, DeSelectBlock, and ClearSelection.
    
    // Is there any selection, if selecting, includes the active selection block
    //   which is not yet part of underlying selection system
    virtual bool HasSelection(bool selecting = true) const;
    // Are these coords within either the selecting block or selection
    virtual bool IsCellSelected( const wxSheetCoords& coords ) const;
    virtual bool IsRowSelected( int row ) const;
    virtual bool IsColSelected( int col ) const;
    virtual bool IsBlockSelected( const wxSheetBlock& block ) const;
    // Are we currently in the middle of a selection
    bool IsSelecting() const;

    void SetSelectionMode(wxSheetSelectionMode_Type selmode);
    int  GetSelectionMode() const;
    bool HasSelectionMode(int mode);

    virtual bool SelectRow( int row, bool addToSelected = false, bool sendEvt = false );
    virtual bool SelectRows( int rowTop, int rowBottom, bool addToSelected = false, bool sendEvt = false );
    virtual bool SelectCol( int col, bool addToSelected = false, bool sendEvt = false );
    virtual bool SelectCols( int colLeft, int colRight, bool addToSelected = false, bool sendEvt = false );
    virtual bool SelectCell( const wxSheetCoords& coords, bool addToSelected = false, bool sendEvt = false );
    virtual bool SelectBlock( const wxSheetBlock& block, bool addToSelected = false, bool sendEvt = false );
    // selects everything to numRows, numCols
    virtual bool SelectAll(bool sendEvt = false);

    virtual bool DeselectRow( int row, bool sendEvt = false );
    virtual bool DeselectRows( int rowTop, int rowBottom, bool sendEvt = false );
    virtual bool DeselectCol( int col, bool sendEvt = false );
    virtual bool DeselectCols( int colLeft, int colRight, bool sendEvt = false );
    virtual bool DeselectCell( const wxSheetCoords& coords, bool sendEvt = false );
    virtual bool DeselectBlock( const wxSheetBlock& block, bool sendEvt = false );
    // clears selection, single deselect event numRows, numCols
    virtual bool ClearSelection(bool send_event = false);

    // toggle the selection of a single cell, row, or col 
    // addToSelected applies to a selection only, ignored if a deselection
    virtual bool ToggleCellSelection( const wxSheetCoords& coords, 
                                      bool addToSelected = false, bool sendEvt = false );
    virtual bool ToggleRowSelection( int row, bool addToSelected = false, bool sendEvt = false );
    virtual bool ToggleColSelection( int col, bool addToSelected = false, bool sendEvt = false );
    
    // Get a pointer to the selection mechanism. You are free to do what you 
    //  want with it, do a ForceRefresh to update the grid when done.
    wxSheetSelection* GetSelection() const;
    
    // During a selection this is the selecting block, else empty
    const wxSheetBlock& GetSelectingBlock() const;
    const wxSheetCoords& GetSelectingAnchor() const;

    // These are internal use functions to highlight a block during mouse
    //  dragging or keyboard selecting
    void SetSelectingBlock(const wxSheetBlock& selectingBlock);
    void SetSelectingAnchor(const wxSheetCoords& selectingAnchor);
    
    // while selecting set and draw m_selectingBlock highlight and clear up last
    virtual void HighlightSelectingBlock( const wxSheetBlock& selectingBlock );
    void HighlightSelectingBlock( const wxSheetCoords& cornerCell,
                                  const wxSheetCoords& otherCell );
    
    // ------------------------------------------------------------------------
    // Copy/Paste functionality for strings (Experimental)
    
    // Copy the current selection using CopyCurrentSelectionInternal then
    //  to the wxClipboard using CopyInternalSelectionToClipboard
    bool CopyCurrentSelectionToClipboard(bool copy_cursor = true,
                                         const wxChar& colSep = wxT('\t'));
    // Copy the current selection to an internal copied selection mechanism 
    //  storing both the positions and values of the selected cells, if no 
    //  selection and copy_cursor then just copy the cursor value
    bool CopyCurrentSelectionInternal(bool copy_cursor = true);
    // Copy the internal selection to the wxClipboard as both a string using 
    //  colSep to separate columns and as an internal representation for 
    //  pasting back into the wxSheet.
    bool CopyInternalSelectionToClipboard(const wxChar& colSep = wxT('\t'));
    // Returns the internal selection as a suitable string to be put into the clipboard.
    //   uses colSep for cols and \n for rows, called by CopySelectionToClipboard
    wxString CopyInternalSelectionToString(const wxChar& colSep = wxT('\t'));

    // Copies the given string (perhaps from the clipboard) to the internal copied 
    //   selection uses colSep for cols and \n for rows, used by PasteFromClipboard
    bool CopyStringToSelection(const wxString& value, const wxChar& colSep = wxT('\t'));
    
    // Tries to get the clipboard data as wxSheet's clipboard data 
    // representation else use CopyStringToSelection to convert a string 
    //  using colSep as the column separator and \n as row separator.
    //  If coords are wxNullSheetCoords, use current cursor position.
    bool PasteFromClipboard(const wxSheetCoords &topLeft = wxNullSheetCoords,
                            const wxChar& colSep = wxT('\t'));
    // Paste the internal copied selection at the topLeft coords or if 
    //  topLeft = wxNullSheetCoords then if IsSelection use the upper right of 
    //  the current selection and only paste into currently selected cells. 
    //  If no selection the the cursor is the topLeft cell. 
    virtual bool PasteInternalCopiedSelection(const wxSheetCoords &topLeft = wxNullSheetCoords);
    // Are the cells being pasted right now, use this in the table's 
    //    SetCellValue and AppendXXX to differentiate between a user typing
    bool CurrentlyPasting() const;
    
    // ------------------------------------------------------------------------
    // Edit control functions (mostly used internally)
    
    // Is/Make the whole sheet editable or readonly 
    // FIXME - make EnableEditing an enum for the different windows
    bool IsEditable() const { return GetSheetRefData()->m_editable; }
    void EnableEditing( bool edit );

    // enable and show the editor control at the coords, returns sucess, ie. !vetoed
    bool EnableCellEditControl( const wxSheetCoords& coords );
    // hide and disable the editor and save the value if save_value, returns sucess, ie. !vetoed
    bool DisableCellEditControl( bool save_value );
    // is this cell valid and editable
    bool CanEnableCellControl(const wxSheetCoords& coords) const;
    // is the cell editor created (may not be shown though)
    bool IsCellEditControlCreated() const;
    // is the cell editor valid and shown
    bool IsCellEditControlShown() const;

    // Create and show the appropriate editor at the EnableCellEditControl coords
    //  this is called internally by EnableCellEditControl, but if you call 
    //  HideCellEditControl and if IsCellEditControlCreated then you can reshow 
    //  it with this, returns sucess
    bool ShowCellEditControl();
    // Hide the editor, doesn't destroy it (use DisableCellEditControl)
    //  check if IsCellEditControlShown first, returns sucess
    bool HideCellEditControl();
    // Save the value of the editor, check IsCellEditControlEnabled() first
    void SaveEditControlValue();

    // Get the current editor, !Ok() if !IsCellEditControlCreated()
    const wxSheetCellEditor& GetEditControl() const { return GetSheetRefData()->m_cellEditor; }
    // These are the coords of the editor, check IsCellEditControlCreated before using
    const wxSheetCoords& GetEditControlCoords() const { return GetSheetRefData()->m_cellEditorCoords; }
    
    // ------------------------------------------------------------------------
    // Drawing functions
    
    // Code that does a lot of grid modification can be enclosed
    // between BeginBatch() and EndBatch() calls to avoid screen flicker
    // EndBatch's refresh = false will not refresh when batchCount is 0
    void BeginBatch();
    void EndBatch(bool refresh=true);
    int  GetBatchCount();
    
    // Use ForceRefresh, rather than wxWindow::Refresh(), to force an
    // immediate repainting of the grid. No effect if GetBatchCount() > 0
    // This function is necessary because wxSheet has a minimal OnPaint()
    // handler to reduce screen flicker.
    void ForceRefresh();
    
    // *** Use these redrawing functions to ensure refed sheets are redrawn ***
    
    // Refresh a single cell, can also draw cells for labels using -1 notation
    // does nothing if cell !visible, or GetBatchCount != 0
    // if single_cell then literally draw only the single cell, else draw the
    // cell to left in case the overflow marker needs to be drawn and the 
    // cells to the right in case this cell overflows.
    void RefreshCell(const wxSheetCoords& coords, bool single_cell = true);
    // Refresh a block of cells in any/all of the windows by chopping up the block, 
    //   uses -1 notation to refresh labels
    void RefreshBlock(const wxSheetBlock& block);
    // Refresh a single row, row = -1 refreshes all col labels, 
    // does nothing if row !visible, or GetBatchCount != 0
    void RefreshRow(int row);
    // Refresh a single col, col = -1 refreshes all row labels, 
    // does nothing if col !visible, or GetBatchCount != 0
    void RefreshCol(int col);
    // Refresh is called using a rect surrounding the block
    // does nothing if block IsEmpty, !visible, or GetBatchCount != 0
    void RefreshGridCellBlock( const wxSheetBlock& block );
    // After SetAttr call this can appropriately refresh the wxSheet areas
    void RefreshAttrChange(const wxSheetCoords& coords, wxSheetAttr_Type type);

    // ************************************************************************
    // Drawing implementation - not for general use

    // Refresh an area of the window that calculates the smaller rects for
    //  each individual window (row/col/corner...) and calls Refresh(subRect)
    //  The rect is the logical rect, not the scrolled device rect
    virtual void Refresh(bool eraseb = true, const wxRect* rect = NULL);
    
    // These directly call wxWindow::Refresh for the appropriate windows
    //   The input rect doesn't have to be clipped to the visible window since
    //   this function takes care of that, but it should be in client coords. 
    void RefreshGridWindow(bool eraseb = true, const wxRect* rect = NULL);
    void RefreshRowLabelWindow(bool eraseb = true, const wxRect* rect = NULL);
    void RefreshColLabelWindow(bool eraseb = true, const wxRect* rect = NULL);
    void RefreshCornerLabelWindow(bool eraseb = true, const wxRect* rect = NULL);

    //    Don't use these if you plan to use the splitter since they only act 
    //    on this sheet.

    // These functions are called by the OnPaint handler of these windows
    //   use these to add "extra touches" before or after redrawing.
    //   The dc should be prepared before calling these.
    virtual void PaintGridWindow( wxDC& dc, const wxRegion& reg );
    virtual void PaintRowLabelWindow( wxDC& dc, const wxRegion& reg );
    virtual void PaintColLabelWindow( wxDC& dc, const wxRegion& reg );
    virtual void PaintCornerLabelWindow( wxDC& dc, const wxRegion& reg );
    virtual void PaintSheetWindow( wxDC& dc, const wxRegion& reg );
    
    // draws a bunch of blocks of grid cells onto the given DC
    virtual void DrawGridCells( wxDC& dc, const wxSheetSelection& blockSel );
    // Draw the area below and to right of grid up to scrollbars
    virtual void DrawGridSpace( wxDC& dc );
    // draw the border around a single cell
    virtual void DrawCellBorder( wxDC& dc, const wxSheetCoords& coords );
    // Draw all the grid lines in the region
    virtual void DrawAllGridLines( wxDC& dc, const wxRegion& reg );
    // Draw a single cell
    virtual void DrawCell( wxDC& dc, const wxSheetCoords& coords );
    // Calls DrawCursorCellHighlight if contained within this selection
    virtual void DrawCursorHighlight( wxDC& dc, const wxSheetSelection& blockSel );
    // Draw the cursor cell highlight
    virtual void DrawCursorCellHighlight(wxDC& dc, const wxSheetCellAttr &attr);

    // draw wxSheetRowLabelWindow labels
    virtual void DrawRowLabels( wxDC& dc, const wxArrayInt& rows );
    // draw wxSheetColLabelWindow labels
    virtual void DrawColLabels( wxDC& dc, const wxArrayInt& cols );
    // draw wxSheetCornerLabelWindow label
    virtual void DrawCornerLabel( wxDC& dc );

    // Draw the row/col resizing marker and if newDragPos != -1, set the 
    //  new position of the marker
    virtual void DrawRowColResizingMarker( int newDragPos = -1 );

    // Draw the splitter button in the rectangle
    virtual void DrawSplitterButton(wxDC &dc, const wxRect& rect);

    // Calculate the Row/ColLabels and Cells exposed for the wxRegion
    //   returns false if none, used for redrawing windows
    bool CalcRowLabelsExposed( const wxRegion& reg, wxArrayInt& rows ) const;
    bool CalcColLabelsExposed( const wxRegion& reg, wxArrayInt& cols ) const;
    bool CalcCellsExposed( const wxRegion& reg, wxSheetSelection& blockSel ) const;
    int  FindOverflowCell( const wxSheetCoords& coords, wxDC& dc );

    // helper drawing functions
    void DrawTextRectangle( wxDC& dc, const wxString& value, const wxRect& rect,
                            int alignment = wxALIGN_LEFT|wxALIGN_TOP,
                            int textOrientation = wxHORIZONTAL );

    void DrawTextRectangle( wxDC& dc, const wxArrayString& lines, const wxRect&,
                            int alignment = wxALIGN_LEFT|wxALIGN_TOP,
                            int textOrientation = wxHORIZONTAL );

    // Split string by '\n' and add to array, returning the number of lines
    //  returns 0 for empty string.
    int StringToLines( const wxString& value, wxArrayString& lines ) const;
    // Get the size of the lines drawn horizontally, returns true if size > 0
    bool GetTextBoxSize( wxDC& dc, const wxArrayString& lines,
                         long *width, long *height ) const;

    // ------------------------------------------------------------------------
    // Geometry utility functions, pixel <-> cell etc
    
    // Note that all of these functions work with the logical coordinates of
    // grid cells and labels so you will need to convert from device
    // coordinates for mouse events etc. 
    // clipToMinMax means that the return value will be within the grid cells 
    // if !clipToMinMax and out of bounds it returns -1.
    // Use ContainsGridXXX to verify validity, -1 doesn't mean label
    wxSheetCoords XYToGridCell( int x, int y, bool clipToMinMax = false ) const;
    int YToGridRow( int y, bool clipToMinMax = false ) const;
    int XToGridCol( int x, bool clipToMinMax = false ) const;

    // return the row/col number that the x/y coord is near the edge of, or
    // -1 if not near an edge. edge_size is +- pixels to cell edge
    // Use ContainsGridXXX to verify validity, -1 doesn't mean label
    int YToEdgeOfGridRow( int y, int edge_size = WXSHEET_LABEL_EDGE_ZONE ) const;
    int XToEdgeOfGridCol( int x, int edge_size = WXSHEET_LABEL_EDGE_ZONE ) const;

    // Get a rect bounding the cell, handles spanning cells and the label 
    //  windows using the -1 notation, getDeviceRect calls CalcScrolledRect
    wxRect CellToRect( const wxSheetCoords& coords, bool getDeviceRect = false ) const;
    // Get a rect bounding the block, handles label windows using the -1 notation, 
    //  getDeviceRect calls CalcScrolledRect
    wxRect BlockToRect( const wxSheetBlock& block, bool getDeviceRect = false ) const;

    // Expand the block by unioning with intersecting spanned cells
    wxSheetBlock ExpandSpannedBlock( const wxSheetBlock& block ) const;
    
    // Convert the block of cells into a wxRect in device coords, expands the
    //  block to contain spanned cells if expand_spanned. 
    //  These functions do handle label cells, but if you span the block from a label
    //  into the grid then the rect will overlap the windows, probably not what you want.
    wxRect BlockToDeviceRect( const wxSheetBlock& block, bool expand_spanned = true ) const; 
    wxRect BlockToLogicalRect( const wxSheetBlock& block, bool expand_spanned = true ) const;

    // Convert the rect in pixels into a block of cells for the grid
    //   if wholeCell then only include cells in the block that are 
    //   wholly contained by the rect
    wxSheetBlock LogicalGridRectToBlock(const wxRect &rect, bool wholeCell = false) const;

    // get a block containing all the currently (partially/fully) visible cells
    wxSheetBlock GetVisibleGridCellsBlock(bool wholeCellVisible = false) const;

    // Align the size of an object inside the rect using wxALIGN enums
    //   if inside then align it to the left if it would have overflown
    //   always pins size to left hand side
    static wxPoint AlignInRect( int align, const wxRect& rect, const wxSize& size, bool inside=true );
        
    // ------------------------------------------------------------------------
    // Scrolling for the window, everything is done with pixels
    //   there is no need for scroll units and they only cause sizing problems

    // Get the scrolled origin of the grid in pixels
    const wxPoint& GetGridOrigin() const { return m_gridOrigin; }
    // Set the absolute scrolled origin of the grid window in pixels 
    //  this checks validity and ensures proper positioning. 
    //  Use x or y = -1 to not change the origin in the x or y direction
    //  Unless setting from a scrollbar event use adjustScrollBars=true
    virtual void SetGridOrigin(int x, int y, bool adjustScrollBars = true, bool sendEvt=false);
    void SetGridOrigin(const wxPoint& pt, bool adjustScrollBars = true, bool sendEvt=false);
        
    // Get the virtual size of the grid in pixels, includes extra width/height,
    //   but does not include the row/col labels width/height.
    wxSize GetGridVirtualSize(bool add_margin=true) const;

    // Get the full size of the sheet which is the width/height of the row/col
    //   labels + the virtual size of the grid.
    wxSize GetSheetVirtualSize(bool add_margin=true) const;

    // Get the extent of the grid, which is the max of the virtual size and 
    //  actual grid window size. Therefore, this may be larger than the virtual
    //  size if the grid is smaller than the containing window. 
    wxSize GetGridExtent() const;

    // Same as wxScrolledWindow Calc(Un)ScrolledPosition
    void CalcScrolledPosition(int x, int y, int *xx, int *yy) const;
    void CalcUnscrolledPosition(int x, int y, int *xx, int *yy) const;
    wxPoint CalcScrolledPosition(const wxPoint& pt) const;
    wxPoint CalcUnscrolledPosition(const wxPoint& pt) const;

    // returns the scrolled position of the rect, logical -> device coords
    wxRect CalcScrolledRect(const wxRect &r) const;
    // returns the unscrolled position of the rect, device -> logical coords
    wxRect CalcUnscrolledRect(const wxRect &r) const;

    // Adjust the scrollbars to match the size/origin of the grid window
    //   call this after SetScrollBarMode
    virtual void AdjustScrollbars(bool calc_win_sizes = true);

    enum SB_Mode
    {
        SB_AS_NEEDED    = 0x0,  // Show the scrollbars as needed
        SB_HORIZ_NEVER  = 0x1,  // Never show horiz scrollbar, even if needed  
        SB_VERT_NEVER   = 0x2,  // Never show vert scrollbar, even if needed  
        SB_NEVER        = SB_HORIZ_NEVER | SB_VERT_NEVER,  
        SB_HORIZ_ALWAYS = 0x4,  // Always show horiz scrollbar
        SB_VERT_ALWAYS  = 0x8,  // Always show vert scrollbar
        SB_ALWAYS       = SB_HORIZ_ALWAYS | SB_VERT_ALWAYS, 
        
        SB_HORIZ_MASK   = SB_HORIZ_NEVER|SB_HORIZ_ALWAYS,
        SB_VERT_MASK    = SB_VERT_NEVER|SB_VERT_ALWAYS
    };
    
    int GetScrollBarMode() const;
    void SetScrollBarMode(int mode);
    void SetHorizontalScrollBarMode(int mode);
    void SetVerticalScrollBarMode(int mode);

    bool NeedsVerticalScrollBar()   const;
    bool NeedsHorizontalScrollBar() const;
    
    // SetDeviceOrigin for the wxDC as appropriate for these windows
    
    virtual void PrepareGridDC( wxDC& dc );
    virtual void PrepareRowLabelDC( wxDC& dc );
    virtual void PrepareColLabelDC( wxDC& dc );

    // ------------------------------------------------------------------------
    // Splitting of the grid window - note that the sheet does not split at all
    //   and that only a wxEVT_SHEET_SPLIT_BEGIN event is sent to notify the 
    //   parent that splitting should take place, see wxSheetSplitter.
    //   The "splitter" is just two small rectangles at the top of the vertical 
    //   scrollbar and right of the horizontal scrollbar. They're only shown
    //   when the scrollbars are shown and if splitting is enabled. 
    //   Call CalcWindowSizes after setting to update the display.

    // Are the splitter buttons enabled to be shown as necessary
    bool GetEnableSplitVertically()   const;
    bool GetEnableSplitHorizontally() const;
    // Enable or disable showing the splitter buttons
    void EnableSplitVertically(bool can_split);
    void EnableSplitHorizontally(bool can_split);
    
    // ------------------------------------------------------------------------
    // implementation

    // helper function to set only the horiz or vert component of orig_align
    //   returns modified alignment, doesn't modify any bits not in wxAlignment
    //   use -1 for hAlign/vAlign to not modify that direction
    static int SetAlignment(int orig_align, int hAlign, int vAlign);

    // Do any of the windows of the wxSheet have the focus?
    bool HasFocus() const;
    
    // Accessors for component windows
    wxSheetChildWindow* GetGridWindow()        const;
    wxSheetChildWindow* GetRowLabelWindow()    const;
    wxSheetChildWindow* GetColLabelWindow()    const;
    wxSheetChildWindow* GetCornerLabelWindow() const;
    // Get the window with these coords, uses -1 notation
    wxWindow* GetWindowForCoords( const wxSheetCoords& coords ) const;

    // ------ event handlers
    void OnMouse( wxMouseEvent& event );
    void OnMouseWheel( wxMouseEvent& event );
    
    void ProcessSheetMouseEvent( wxMouseEvent& event );
    void ProcessRowLabelMouseEvent( wxMouseEvent& event );
    void ProcessColLabelMouseEvent( wxMouseEvent& event );
    void ProcessCornerLabelMouseEvent( wxMouseEvent& event );
    void ProcessGridCellMouseEvent( wxMouseEvent& event );
    
    void OnScroll( wxScrollEvent& event );

    // End the row/col dragging, returns true if width/height have changed
    bool DoEndDragResizeRowCol();

    // ------ control types
    enum 
    { 
        wxSHEET_TEXTCTRL = 2100,
        wxSHEET_CHECKBOX,
        wxSHEET_CHOICE,
        wxSHEET_COMBOBOX 
    };
    
    enum 
    {
        ID_HORIZ_SCROLLBAR = 1,
        ID_VERT_SCROLLBAR,
        ID_MOUSE_DRAG_TIMER,
        ID_GRID_WINDOW,
        ID_ROW_LABEL_WINDOW,
        ID_COL_LABEL_WINDOW,
        ID_CORNER_LABEL_WINDOW
    };

    virtual void CalcWindowSizes(bool adjustScrollBars = true);
    virtual void Fit(); // overridden wxWindow methods

    // Get the ref counted data the sheet uses, *please* try to not access this
    //  directly if a functions exists to do it for you.
    wxSheetRefData* GetSheetRefData() const;
    
    // Create and send wxSheetXXXEvent depending on type and fill extra data
    //   from a wxKeyEvent or wxMouseEvent (if NULL all keydown are set false)
    // returns EVT_VETOED/SKIPPED/CLAIMED
    enum 
    {
        EVT_VETOED  = -1,  // veto was called on the event
        EVT_SKIPPED = 0,   // no evt handler found or evt was Skip()ed
        EVT_CLAIMED = 1    // event was handled and not Skip()ed
    };
    int SendEvent( const wxEventType type, const wxSheetCoords& coords, 
                   wxEvent* mouseOrKeyEvt = NULL, 
                   const wxString& cmdString = wxEmptyString, int cmd_int = 0);
    int SendCellSizeEvent( const wxEventType type, const wxSheetCoords& coords,
                           int new_size, wxEvent* mouseOrKeyEvt = NULL );
    int SendRangeSelectEvent( const wxEventType type, const wxSheetBlock& block,
                              bool selecting, bool add, wxEvent* mouseOrKeyEvt = NULL );
    int SendEditorCreatedEvent( const wxEventType type, const wxSheetCoords& coords, 
                                wxWindow* ctrl );
        
    // Just send the event returning EVT_VETOED/SKIPPED/CLAIMED
    int DoSendEvent( wxSheetEvent* event );

    enum MouseCursorMode
    {
        WXSHEET_CURSOR_SELECT_CELL = 0x0001,
        WXSHEET_CURSOR_SELECT_ROW  = 0x0002,
        WXSHEET_CURSOR_SELECT_COL  = 0x0004,
        WXSHEET_CURSOR_SELECTING   = WXSHEET_CURSOR_SELECT_CELL|WXSHEET_CURSOR_SELECT_ROW|WXSHEET_CURSOR_SELECT_COL,
        WXSHEET_CURSOR_RESIZE_ROW  = 0x0008,
        WXSHEET_CURSOR_RESIZE_COL  = 0x0010,
        WXSHEET_CURSOR_RESIZING    = WXSHEET_CURSOR_RESIZE_ROW|WXSHEET_CURSOR_RESIZE_COL,
        WXSHEET_CURSOR_SPLIT_VERTICAL   = 0x0020,
        WXSHEET_CURSOR_SPLIT_HORIZONTAL = 0x0040,
        WXSHEET_CURSOR_SPLITTING        = WXSHEET_CURSOR_SPLIT_VERTICAL|WXSHEET_CURSOR_SPLIT_HORIZONTAL
    };
    // Set the m_mouseCursor for the wxCursor and m_mouseCursorMode for behavior
    // you should always use it and not set m_mouseCursor[Mode] directly!
    void SetMouseCursorMode( MouseCursorMode mode, wxWindow *win );
    // Get the mouse cursor mode, &ed with mask, default returns original value
    int GetMouseCursorMode(int mask = ~0) const { return (m_mouseCursorMode & mask); }
    // Is the mouse cursor in the mode?
    bool HasMouseCursorMode(int mode) const { return GetMouseCursorMode(mode) != 0; }
    
    // Set the window that has capture, releases the previous one if necessary
    // always use this, set with NULL to release mouse
    void SetCaptureWindow( wxWindow *win );
    wxWindow *GetCaptureWindow() const;
    
    %extend {
		wxWindow* CastAsWxWindow()
		{
			return static_cast<wxWindow*>(self);
		}
	}

    %extend {
		wxEvtHandler* CastAsWxEvtHandler()
		{
			return static_cast<wxEvtHandler*>(self);
		}
	}
    
};

// ----------------------------------------------------------------------------
// wxSheetEvent
// ----------------------------------------------------------------------------
class wxSheetEvent : public wxNotifyEvent
{
public:
    wxSheetEvent(wxWindowID id = 0, wxEventType type = wxEVT_NULL, 
                 wxObject* obj = NULL,
                 const wxSheetCoords &coords = wxNullSheetCoords, 
                 const wxPoint &pos = wxPoint(-1, -1), bool sel = true);

    wxSheetEvent(const wxSheetEvent& event) : wxNotifyEvent(event), 
                     m_coords(event.m_coords), 
                     m_pos(event.m_pos), m_scrPos(event.m_scrPos),
                     m_selecting(event.m_selecting), 
                     m_control(event.m_control), m_shift(event.m_shift),
                     m_alt(event.m_alt), m_meta(event.m_meta), 
                     m_evtWin(event.m_evtWin) { }

    int  GetRow() const { return m_coords.m_row; }
    int  GetCol() const { return m_coords.m_col; }
    const wxSheetCoords& GetCoords() const { return m_coords; }
    const wxPoint& GetPosition() const { return m_pos; }
    bool Selecting()   const { return m_selecting; }
    bool ControlDown() const { return m_control; }
    bool ShiftDown()   const { return m_shift; }
    bool AltDown()     const { return m_alt; }
    bool MetaDown()    const { return m_meta; }

    // Get the event relative to the window that it occured in.
    //   Scrolls the position so the pt is relative to the top left.
    const wxPoint& GetScrolledPosition() const { return m_scrPos; }
    // Get the window that the event originally occured in.
    //   (for mouse and key events) 
    //   example for wxEVT_SHEET_CELL_RIGHT_UP
    //   if (evt.GetEventWindow()) 
    //       evt.GetEventWindow()->PopupMenu(menu, evt.GetScrolledPosition());
    wxWindow* GetEventWindow() const { return m_evtWin; }

    // implementation
    
    // Setup the Ctrl/Shift/Alt/Meta keysDown from a wxKeyEvent or wxMouseEvent
    // Also sets mouse position, but the GetEventObject must be of type wxSheet
    bool SetKeysDownMousePos(wxEvent *mouseOrKeyEvent);

    virtual wxEvent *Clone() const { return new wxSheetEvent(*this); }
    
    wxSheetCoords m_coords;
    wxPoint       m_pos;
    wxPoint       m_scrPos;
    bool m_selecting;
    bool m_control;
    bool m_shift;
    bool m_alt;
    bool m_meta;
    wxWindow *m_evtWin;
};

// ----------------------------------------------------------------------------
// wxSheetCellSizeEvent - wxEVT_SHEET_ROW/COL_SIZE/ING/ED
// ----------------------------------------------------------------------------
class wxSheetCellSizeEvent : public wxSheetEvent
{
public:
    wxSheetCellSizeEvent( wxWindowID id = 0, wxEventType type = wxEVT_NULL, 
                          wxObject* obj = NULL, 
                          const wxSheetCoords &coords = wxNullSheetCoords,
                          int size = 0 );

    wxSheetCellSizeEvent(const wxSheetCellSizeEvent& event) 
        : wxSheetEvent(event) { }

    int GetSize() const { return GetInt(); }
   
    // implementation
    virtual wxEvent *Clone() const { return new wxSheetCellSizeEvent(*this); }
};

class wxSheetRangeSelectEvent : public wxSheetEvent
{
public:
    wxSheetRangeSelectEvent( wxWindowID id = 0, wxEventType type = wxEVT_NULL, 
                             wxObject* obj = NULL,
                             const wxSheetBlock& block = wxNullSheetBlock, 
                             bool sel = false, bool add_to_sel = false );

    wxSheetRangeSelectEvent(const wxSheetRangeSelectEvent& event) 
        : wxSheetEvent(event), m_block(event.m_block), m_add(event.m_add) { }

    const wxSheetBlock& GetBlock() const { return m_block; }
    bool GetAddToSelection() const       { return m_add; }
    
    void SetBlock( const wxSheetBlock& block ) { m_block = block; }

    // wxPoint GetPosition() is unused
    // int GetCoords/Row/Col() is unused
    
    // implementation
    virtual wxEvent *Clone() const { return new wxSheetRangeSelectEvent(*this); }
    
    wxSheetBlock m_block;
    bool m_add;
};

class wxSheetEditorCreatedEvent : public wxCommandEvent 
{
public:
    wxSheetEditorCreatedEvent( wxWindowID id = 0, wxEventType type = wxEVT_NULL, 
                               wxObject* obj = NULL,
                               const wxSheetCoords& coords = wxNullSheetCoords, 
                               wxWindow* ctrl = NULL );

    wxSheetEditorCreatedEvent(const wxSheetEditorCreatedEvent& evt) 
        : wxCommandEvent(evt), m_coords(evt.m_coords), m_ctrl(evt.m_ctrl) { }


    const wxSheetCoords& GetCoords() const { return m_coords; }
    wxWindow* GetControl() const           { return m_ctrl; }
    
    void SetCoords(const wxSheetCoords& coords) { m_coords = coords; }
    void SetControl(wxWindow* ctrl)             { m_ctrl = ctrl; }

    // implementation
    virtual wxEvent *Clone() const { return new wxSheetEditorCreatedEvent(*this); }

    wxSheetCoords m_coords;
    wxWindow*     m_ctrl;
};

class wxSheetCellAttr : public wxObject
{
public:

    // if create then create with ref data
    wxSheetCellAttr( bool create = false );
    // make a refed copy of the other attribute
    wxSheetCellAttr( const wxSheetCellAttr& attr ) : wxObject() { Ref(attr); }

    // Recreate the ref data, unrefing the old
    bool Create();
    void Destroy() { UnRef(); }
    inline bool Ok() const { return m_refData != NULL; }

    // Makes a full new unrefed copy of the other, this doesn't have to be created
    bool Copy(const wxSheetCellAttr& other);
    // Copies the values from the other, but only if the other has them, this must be created
    bool UpdateWith(const wxSheetCellAttr& other);
    // Merges this with the other, copy values of other only this doesn't have them
    bool MergeWith(const wxSheetCellAttr &mergefrom);
    
    // setters
    void SetForegroundColour(const wxColour& foreColour);
    void SetBackgroundColour(const wxColour& backColour);
    void SetFont(const wxFont& font);
    // wxSheetAttrAlign_Type
    void SetAlignment(int align);
    void SetAlignment(int horzAlign, int vertAlign);
    // wxSheetAttrOrientation_Type
    void SetOrientation(int orientation);
    void SetLevel(wxSheetAttrLevel_Type level);
    void SetOverflow(bool allow);
    void SetOverflowMarker(bool draw_marker);
    void SetShowEditor(bool show_editor);
    void SetReadOnly(bool isReadOnly);
    void SetRenderer(const wxSheetCellRenderer& renderer);
    void SetEditor(const wxSheetCellEditor& editor);
    void SetKind(wxSheetAttr_Type kind);

    // validation
    bool HasForegoundColour() const;
    bool HasBackgroundColour() const;
    bool HasFont() const;
    bool HasAlignment() const;
    bool HasOrientation() const;
    bool HasLevel() const;
    bool HasOverflowMode() const;
    bool HasOverflowMarkerMode() const;
    bool HasShowEditorMode() const;
    bool HasReadWriteMode() const;
    bool HasRenderer() const;
    bool HasEditor() const;
    bool HasDefaultAttr() const;
    // bool HasKind() const - always has kind, default is wxSHEET_AttrCell

    // does this attr define all the HasXXX properties, except DefaultAttr
    //   if this is true, it's a suitable default attr for an area
    bool IsComplete() const;  

    // accessors
    const wxColour& GetForegroundColour() const;
    const wxColour& GetBackgroundColour() const;
    const wxFont& GetFont() const;
    int GetAlignment() const;
    wxOrientation GetOrientation() const;
    wxSheetAttrLevel_Type GetLevel() const;
    bool GetOverflow() const;
    bool GetOverflowMarker() const;
    bool GetShowEditor() const;
    bool GetReadOnly() const;
    wxSheetCellRenderer GetRenderer(wxSheet* grid, const wxSheetCoords& coords) const;
    wxSheetCellEditor GetEditor(wxSheet* grid, const wxSheetCoords& coords) const;
    wxSheetAttr_Type GetKind() const;

    // any unset values of this attr are retrieved from the default attr
    // if you try to set the def attr to this, it's ignored
    // don't bother to link multiple attributes together in a loop, obviously.
    const wxSheetCellAttr& GetDefaultAttr() const;
    void SetDefaultAttr(const wxSheetCellAttr& defaultAttr);

    // operators
    bool operator == (const wxSheetCellAttr& obj) const { return m_refData == obj.m_refData; }
    bool operator != (const wxSheetCellAttr& obj) const { return m_refData != obj.m_refData; }
    
    wxSheetCellAttr Clone() const     { wxSheetCellAttr obj; obj.Copy(*this); return obj; }
    wxSheetCellAttr* NewClone() const { return new wxSheetCellAttr(Clone()); }

    // implementation
    void SetType(int type, int mask);
    int  GetType(int mask = ~0) const;
    bool HasType(int type) const { return GetType(type) != 0; }
};

class wxSheetCellEditor
{
public:

    wxSheetCellEditor( wxSheetCellEditorRefData *editor = NULL );
    wxSheetCellEditor( const wxSheetCellEditor& editor ) { Ref(editor); }

    void Destroy() { UnRef(); }
    bool Ok() const { return m_refData != NULL; }
    
    bool IsCreated() const;
    bool IsShown() const;
    
    wxWindow* GetControl() const;
    void SetControl(wxWindow* control);
    void DestroyControl();

    void CreateEditor(wxWindow* parent, wxWindowID id, 
                      wxEvtHandler* evtHandler, wxSheet* sheet);

    void SetSize(const wxRect& rect, const wxSheetCellAttr& attr);
    wxSize GetBestSize(wxSheet& sheet, const wxSheetCellAttr& attr,
                       const wxSheetCoords& coords) const;
    void Show(bool show, const wxSheetCellAttr &attr);
    void PaintBackground(wxSheet& sheet, const wxSheetCellAttr& attr, 
                         wxDC& dc, const wxRect& rect, 
                         const wxSheetCoords& coords, bool isSelected);
    
    void InitEditor(const wxSheetCoords& coords, const wxSheetCellAttr& attr, 
                    wxSheet* sheet);
    void BeginEdit(const wxSheetCoords& coords, wxSheet* sheet);
    bool EndEdit(const wxSheetCoords& coords, wxSheet* sheet);
    void ResetValue();

    bool IsAcceptedKey(wxKeyEvent& event);
    void StartingKey(wxKeyEvent& event);
    void StartingClick();
    void HandleReturn(wxKeyEvent& event);

    bool OnKeyDown(wxKeyEvent& event);
    bool OnChar(wxKeyEvent& event);

    void SetParameters(const wxString& params);
    
    wxString GetValue() const;
    wxString GetInitValue() const;

    bool Copy(const wxSheetCellEditor& other);    
    
    // operators
    bool operator == (const wxSheetCellEditor& obj) const { return m_refData == obj.m_refData; }
    bool operator != (const wxSheetCellEditor& obj) const { return m_refData != obj.m_refData; }
    wxSheetCellEditor Clone() const     { wxSheetCellEditor obj; obj.Copy(*this); return obj; }
    wxSheetCellEditor* NewClone() const { return new wxSheetCellEditor(Clone()); }
};

// The C++ version of wxPySheetCellEditor
%{
class wxPySheetCellEditor : public wxSheetCellEditor
{
public:
    wxPySheetCellEditor() : wxSheetCellEditor() {}

    void Create(wxWindow* parent, wxWindowID id, wxEvtHandler* evtHandler) {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "Create")) {
            PyObject* po = wxPyMake_wxObject(parent,false);
            PyObject* eo = wxPyMake_wxObject(evtHandler,false);

            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OiO)", po, id, eo));
            Py_DECREF(po);
            Py_DECREF(eo);
        }
        wxPyEndBlockThreads(blocked);
    }


    void BeginEdit(int row, int col, wxSheet* grid) {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "BeginEdit")) {
            PyObject* go = wxPyMake_wxObject(grid,false);
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iiO)", row, col, go));
            Py_DECREF(go);
        }
        wxPyEndBlockThreads(blocked);
    }


    bool EndEdit(int row, int col, wxSheet* grid) {
        bool rv = false;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "EndEdit")) {
            PyObject* go = wxPyMake_wxObject(grid,false);
            rv = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iiO)", row, col, go));
            Py_DECREF(go);
        }
        wxPyEndBlockThreads(blocked);
        return rv;
    }


    wxSheetCellEditor* Clone() const {
        wxSheetCellEditor* rval = NULL;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "Clone")) {
            PyObject* ro;
            wxSheetCellEditor* ptr;
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("()"));
            if (ro) {
                if (wxPyConvertSwigPtr(ro, (void **)&ptr, wxT("wxSheetCellEditor")))
                    rval = ptr;
                Py_DECREF(ro);
            }
        }
        wxPyEndBlockThreads(blocked);
        return rval;
    }
    
    void SetSize(const wxRect& rect, const wxSheetCellAttr& attr)
    {
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "SetSize"))) {
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(ii)", rect, attr));
        }
        wxPyEndBlockThreads(blocked);
        if (! found)
            wxSheetCellEditor::SetSize(rect, attr);
    }
    void base_SetSize(const wxRect& rect, const wxSheetCellAttr& attr)
	{
		wxSheetCellEditor::SetSize(rect, attr);
	}

    void Show(bool show, wxSheetCellAttr *attr) {
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "Show"))) {
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(ii)", show, attr));
        }
        wxPyEndBlockThreads(blocked);
        if (! found)
            wxSheetCellEditor::Show(show, attr);
    }
    void base_Show(bool show, wxSheetCellAttr *attr) {
        wxSheetCellEditor::Show(show, attr);
    }


    void PaintBackground(wxSheet& sheet, const wxSheetCellAttr& attr, 
                                        wxDC& dc, const wxRect& rect, 
                                        const wxSheetCoords& coords, bool isSelected) {
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "PaintBackground)"))) {
            PyObject* ro = wxPyConstructObject((void*)&rect, wxT("wxRect"), 0);

            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OO)", ro, attr));

            Py_DECREF(ro);
        }
        wxPyEndBlockThreads(blocked);
        if (! found)
            wxSheetCellEditor::PaintBackground(sheet, attr, dc, rect, coords, isSelected);
    }
    void base_PaintBackground(wxSheet& sheet, const wxSheetCellAttr& attr, 
                                        wxDC& dc, const wxRect& rect, 
                                        const wxSheetCoords& coords, bool isSelected) {
        wxSheetCellEditor::PaintBackground(sheet, attr, dc, rect, coords, isSelected);
    }


    DEC_PYCALLBACK___pure(Reset);
    DEC_PYCALLBACK_bool_any(IsAcceptedKey, wxKeyEvent);
    DEC_PYCALLBACK__any(StartingKey, wxKeyEvent);
    DEC_PYCALLBACK__any(HandleReturn, wxKeyEvent);
    DEC_PYCALLBACK__(StartingClick);
    DEC_PYCALLBACK__(Destroy);
    DEC_PYCALLBACK__STRING(SetParameters);
    DEC_PYCALLBACK_STRING__constpure(GetValue);

    PYPRIVATE;
};


IMP_PYCALLBACK__STRING( wxPySheetCellEditor, wxSheetCellEditor, SetParameters);
IMP_PYCALLBACK___pure(wxPySheetCellEditor, wxSheetCellEditor, Reset);
IMP_PYCALLBACK_bool_any(wxPySheetCellEditor, wxSheetCellEditor, IsAcceptedKey, wxKeyEvent);
IMP_PYCALLBACK__any(wxPySheetCellEditor, wxSheetCellEditor, StartingKey, wxKeyEvent);
IMP_PYCALLBACK__any(wxPySheetCellEditor, wxSheetCellEditor, HandleReturn, wxKeyEvent);
IMP_PYCALLBACK__(wxPySheetCellEditor, wxSheetCellEditor, StartingClick);
IMP_PYCALLBACK__(wxPySheetCellEditor, wxSheetCellEditor, Destroy);
IMP_PYCALLBACK_STRING__constpure(wxPySheetCellEditor, wxSheetCellEditor, GetValue);

%}

// Let SWIG know about it so it can create the Python version
class wxPySheetCellEditor : public wxSheetCellEditor {
public:
    %pythonAppend wxPySheetCellEditor  "self._setCallbackInfo(self, PySheetCellEditor)"

    wxPySheetCellEditor();
    void _setCallbackInfo(PyObject* self, PyObject* _class);

    void base_SetSize(const wxRect& rect, const wxSheetCellAttr& attr);
    void base_Show(bool show, wxSheetCellAttr *attr);
    void base_PaintBackground(wxSheet& sheet, const wxSheetCellAttr& attr, 
                                        wxDC& dc, const wxRect& rect, 
                                        const wxSheetCoords& coords, bool isSelected);
    bool base_IsAcceptedKey(wxKeyEvent& event);
    void base_StartingKey(wxKeyEvent& event);
    void base_StartingClick();
    void base_HandleReturn(wxKeyEvent& event);
    void base_Destroy();
    void base_SetParameters(const wxString& params);
};

class wxSheetCellRenderer : public wxObject
{
public:
    wxSheetCellRenderer(wxSheetCellRendererRefData *renderer = NULL);
    wxSheetCellRenderer( const wxSheetCellRenderer& renderer );

    void Destroy();

    bool Ok() const;
    
    // draw the given cell on the provided DC inside the given rectangle
    // using the style specified by the attribute and the default or selected
    // state corresponding to the isSelected value.
    void Draw(wxSheet& sheet, const wxSheetCellAttr& attr, 
              wxDC& dc, const wxRect& rect, 
              const wxSheetCoords& coords, bool isSelected);

    // get the preferred size of the cell for its contents
    wxSize GetBestSize(wxSheet& sheet, const wxSheetCellAttr& attr,
                       wxDC& dc, const wxSheetCoords& coords);

    // interpret renderer parameters: arbitrary string whose interpretation is
    // left to the derived classes
    void SetParameters(const wxString& params);
  
    bool Copy(const wxSheetCellRenderer& other);    

    // operators
    bool operator == (const wxSheetCellRenderer& obj) const { return m_refData == obj.m_refData; }
    bool operator != (const wxSheetCellRenderer& obj) const { return m_refData != obj.m_refData; }

//    wxSheetCellRenderer Clone() const     { wxSheetCellRenderer obj; obj.Copy(*this); return obj; }
    wxSheetCellRenderer* NewClone() const { return new wxSheetCellRenderer(Clone()); }   
};

%{
class wxPySheetCellRenderer : public wxSheetCellRenderer
{
    wxPySheetCellRenderer() : wxSheetCellRenderer() {};

    // Implement Python callback aware virtual methods
    void Draw(wxSheet& grid, wxSheetCellAttr& attr,
              wxDC& dc, const wxRect& rect,
              const wxSheetCoords& coords, bool isSelected) {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "Draw")) {
            PyObject* go = wxPyMake_wxObject(&grid,false);
            PyObject* dco = wxPyMake_wxObject(&dc,false);
            PyObject* ao = wxPyMake_wxObject(&attr,false);
            PyObject* co = SWIG_NewPointerObj((void *)(&coords), SWIGTYPE_p_wxSheetCoords, 0);
            PyObject* ro = wxPyConstructObject((void*)&rect, wxT("wxRect"), 0);

            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OOOOOi)", go, ao, dco, ro,
                                                         co, isSelected));
            Py_DECREF(go);
            Py_DECREF(ao);
            Py_DECREF(dco);
            Py_DECREF(ro);
            Py_DECREF(co);
        }
        wxPyEndBlockThreads(blocked);
    }

    wxSize GetBestSize(wxSheet& grid, wxSheetCellAttr& attr, wxDC& dc,
                       const wxSheetCoords& coords) {
        wxSize rval;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "GetBestSize")) {
            PyObject* ro;
            wxSize*   ptr;
            PyObject* go = wxPyMake_wxObject(&grid,false);
            PyObject* dco = wxPyMake_wxObject(&dc,false);
            PyObject* co = SWIG_NewPointerObj((void *)(&coords), SWIGTYPE_p_wxSheetCoords, 0);
            PyObject* ao = wxPyMake_wxObject(&attr,false);

            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(OOOO)",
                                                                 go, ao, dco,
                                                                 co));
            Py_DECREF(go);
            Py_DECREF(ao);
            Py_DECREF(dco);
            Py_DECREF(co);

            if (ro) {
                const char* errmsg = "GetBestSize should return a 2-tuple of integers or a wxSize object.";
                if (wxPyConvertSwigPtr(ro, (void **)&ptr, wxT("wxSize"))) {
                    rval = *ptr;
                }
                else if (PySequence_Check(ro) && PyObject_Length(ro) == 2) {
                    PyObject* o1 = PySequence_GetItem(ro, 0);
                    PyObject* o2 = PySequence_GetItem(ro, 1);
                    if (PyNumber_Check(o1) && PyNumber_Check(o2))
                        rval = wxSize(PyInt_AsLong(o1), PyInt_AsLong(o2));
                    else
                        PyErr_SetString(PyExc_TypeError, errmsg);
                    Py_DECREF(o1);
                    Py_DECREF(o2);
                }
                else {
                    PyErr_SetString(PyExc_TypeError, errmsg);
                }
                Py_DECREF(ro);
            }
        }
        wxPyEndBlockThreads(blocked);
        return rval;
    }

    wxSheetCellRenderer *NewClone() const {
        wxSheetCellRenderer* rval = NULL;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "NewClone")) {
            PyObject* ro;
            wxSheetCellRenderer* ptr;
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("()"));
            if (ro) {
                if (wxPyConvertSwigPtr(ro, (void **)&ptr, wxT("wxSheetCellRenderer")))
                    rval = ptr;
                Py_DECREF(ro);
            }
        }
        wxPyEndBlockThreads(blocked);
        return rval;
    }

    DEC_PYCALLBACK__STRING(SetParameters);

    PYPRIVATE;
};

IMP_PYCALLBACK__STRING( wxPySheetCellRenderer, wxSheetCellRenderer, SetParameters);
%}

class wxPySheetCellRenderer : public wxSheetCellRenderer
{
    %pythonAppend wxPySheetCellRenderer  "self._setCallbackInfo(self, PySheetCellRenderer)"

    wxPySheetCellRenderer();
    void _setCallbackInfo(PyObject* self, PyObject* _class);

    void base_SetParameters(const wxString& params);
};

class wxSheetTable : public wxObject, public wxClientDataContainer
{
public:
    wxSheetTable( wxSheet *sheet = NULL );
    virtual ~wxSheetTable();

    virtual void SetView( wxSheet *sheet );
    virtual wxSheet* GetView();

    virtual int GetNumberRows();
    virtual int GetNumberCols();
    
    bool ContainsGridRow( int row );
    bool ContainsGridCol( int col );
    bool ContainsGridCell(const wxSheetCoords& coords);
    bool ContainsRowLabelCell( const wxSheetCoords& coords );
    bool ContainsColLabelCell( const wxSheetCoords& coords );
    
    virtual wxString GetValue( const wxSheetCoords& coords );
    virtual void SetValue( const wxSheetCoords& coords, const wxString& value );
    virtual bool HasValue( const wxSheetCoords& coords );
    virtual int GetFirstNonEmptyColToLeft( const wxSheetCoords& coords );

    virtual void ClearValues(int update = wxSHEET_UpdateValues);
        
    wxString GetDefaultRowLabelValue( int row ) const;
    wxString GetDefaultColLabelValue( int col ) const;
        
    virtual long   GetValueAsLong( const wxSheetCoords& coords );
    virtual double GetValueAsDouble( const wxSheetCoords& coords );
    virtual bool   GetValueAsBool( const wxSheetCoords& coords );

    virtual void SetValueAsLong( const wxSheetCoords& coords, long value );
    virtual void SetValueAsDouble( const wxSheetCoords& coords, double value );
    virtual void SetValueAsBool( const wxSheetCoords& coords, bool value );

    virtual void* GetValueAsCustom( const wxSheetCoords& coords, const wxString& typeName );
    virtual void  SetValueAsCustom( const wxSheetCoords& coords, const wxString& typeName, void* value );
    
    virtual bool CanGetValueAs( const wxSheetCoords& coords, const wxString& typeName );
    virtual bool CanSetValueAs( const wxSheetCoords& coords, const wxString& typeName );

    virtual wxString GetTypeName( const wxSheetCoords& coords );

    virtual wxSheetValueProviderBase* GetGridCellValueProvider() const { return m_gridCellValues; }
    virtual wxSheetValueProviderBase* GetRowLabelValueProvider() const { return m_rowLabelValues; }
    virtual wxSheetValueProviderBase* GetColLabelValueProvider() const { return m_colLabelValues; }
    void SetGridCellValueProvider(wxSheetValueProviderBase* gridCellValues, bool is_owner);
    void SetRowLabelValueProvider(wxSheetValueProviderBase* rowLabelValues, bool is_owner);
    void SetColLabelValueProvider(wxSheetValueProviderBase* colLabelValues, bool is_owner);

    virtual wxSheetCellAttr GetAttr( const wxSheetCoords& coords,
                                     wxSheetAttr_Type kind );
    
    virtual void SetAttr( const wxSheetCoords& coords, 
                          const wxSheetCellAttr &attr, 
                          wxSheetAttr_Type kind );

    virtual wxSheetCellAttrProvider* GetAttrProvider() const { return m_attrProvider; }
    void SetAttrProvider(wxSheetCellAttrProvider *attrProvider, bool is_owner);
    
    virtual bool HasSpannedCells();
    virtual wxSheetBlock GetCellBlock( const wxSheetCoords& coords );
    virtual void SetCellSpan( const wxSheetBlock& block );

    virtual wxSheetSelection* GetSpannedBlocks() const { return m_spannedCells; }
    void SetSpannedBlocks(wxSheetSelection *spannedCells, bool is_owner);

    virtual bool UpdateRows( size_t row, int numRows, int update = wxSHEET_UpdateAll );
    virtual bool UpdateCols( size_t col, int numCols, int update = wxSHEET_UpdateAll );

    virtual bool UpdateSheetRowsCols(int update = wxSHEET_UpdateAll );
};

// Python-aware version
%{
class wxPySheetTableBase : public wxSheetTable
{
public:
    wxPySheetTableBase() : wxSheetTable() {}

    PYCALLBACK_INT__pure(GetNumberRows);
    PYCALLBACK_INT__pure(GetNumberCols);
    PYCALLBACK_BOOL_COORD_pure(IsEmptyCell);
    PYCALLBACK_STRING_COORD(wxSheetTable, GetTypeName);
    PYCALLBACK_BOOL_COORDSTRING(wxSheetTable, CanGetValueAs);
    PYCALLBACK_BOOL_COORDSTRING(wxSheetTable, CanSetValueAs);
//    PYCALLBACK__(wxSheetTable, Clear);
//    PYCALLBACK_BOOL_SIZETSIZET(wxSheetTable, InsertRows);
//    PYCALLBACK_BOOL_SIZETSIZET(wxSheetTable, DeleteRows);
//    PYCALLBACK_BOOL_SIZETSIZET(wxSheetTable, InsertCols);
//    PYCALLBACK_BOOL_SIZETSIZET(wxSheetTable, DeleteCols);
//    PYCALLBACK_BOOL_SIZET(wxSheetTable, AppendRows);
//    PYCALLBACK_BOOL_SIZET(wxSheetTable, AppendCols);
//    PYCALLBACK_STRING_INT(wxSheetTable, GetRowLabelValue);
//    PYCALLBACK_STRING_INT(wxSheetTable, GetColLabelValue);
//    PYCALLBACK__INTSTRING(wxSheetTable, SetRowLabelValue);
//    PYCALLBACK__INTSTRING(wxSheetTable, SetColLabelValue);
//    PYCALLBACK_BOOL_(wxSheetTable, CanHaveAttributes);
    PYCALLBACK_GCA_COORDKIND(wxSheetTable, GetAttr);
    PYCALLBACK__GCACOORD(wxSheetTable, SetAttr);
//    PYCALLBACK__GCAINT(wxSheetTable, SetRowAttr);
//    PYCALLBACK__GCAINT(wxSheetTable, SetColAttr);


	void Clear() 
	{ 
		std::cout << "wxPySheetTableBase::Clear" << std::endl;
		GetGridCellValueProvider()->Clear(); 
	}

    wxString GetRowLabelValue( int row ) 
    { 
		std::cout << "wxPySheetTableBase::GetRowLabelValue" << std::endl;
		return GetRowLabelValueProvider()->GetValue( wxSheetCoords(row, 0) ); 
	}
    
    wxString GetColLabelValue( int col ) 
    { 
		std::cout << "wxPySheetTableBase::GetColLabelValue" << std::endl;
		GetColLabelValueProvider()->GetValue( wxSheetCoords(0, col) );
	}

    wxString SetRowLabelValue( int row, const wxString& value ) 
    { 
		std::cout << "wxPySheetTableBase::SetRowLabelValue" << std::endl;
		GetRowLabelValueProvider()->SetValue( wxSheetCoords(row, 0), value ); 
	}
	
    wxString SetColLabelValue( int col, const wxString& value ) 
    { 
		std::cout << "wxPySheetTableBase::SetColLabelValue" << std::endl;
		GetColLabelValueProvider()->SetValue( wxSheetCoords(0, col), value ); 
	}


    wxString GetValue(int row, int col) {
		std::cout << "wxPySheetTableBase::GetValue" << std::endl;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        wxString rval;
        if (wxPyCBH_findCallback(m_myInst, "GetValue")) {
            PyObject* ro;
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(ii)",row,col));
            if (ro) {
                if (!PyString_Check(ro) && !PyUnicode_Check(ro)) {
                    PyObject* old = ro;
                    ro = PyObject_Str(ro);
                    Py_DECREF(old);
                }
                rval = Py2wxString(ro);
                Py_DECREF(ro);
            }
        }
        wxPyEndBlockThreads(blocked);
        return rval;
    }

    void SetValue(int row, int col, const wxString& val) 
    {
		std::cout << "wxPySheetTableBase::SetValue" << std::endl;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "SetValue")) 
        {
            PyObject* s = wx2PyString(val);
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iiO)",row,col,s));
            Py_DECREF(s);
		}
        wxPyEndBlockThreads(blocked);
	}


    // Map the Get/Set methods for the standard non-string types to
    // the GetValue and SetValue python methods.
    long GetValueAsLong( int row, int col ) {
        long rval = 0;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "GetValue")) {
            PyObject* ro;
            PyObject* num;
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(ii)", row, col));
            if (ro && PyNumber_Check(ro)) {
                num = PyNumber_Int(ro);
                if (num) {
                    rval = PyInt_AsLong(num);
                    Py_DECREF(num);
                }
                Py_DECREF(ro);
            }
        }
        wxPyEndBlockThreads(blocked);
        return rval;
    }

    double GetValueAsDouble( int row, int col ) {
        double rval = 0.0;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "GetValue")) {
            PyObject* ro;
            PyObject* num;
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(ii)", row, col));
            if (ro && PyNumber_Check(ro)) {
                num = PyNumber_Float(ro);
                if (num) {
                    rval = PyFloat_AsDouble(num);
                    Py_DECREF(num);
                }
                Py_DECREF(ro);
            }
        }
        wxPyEndBlockThreads(blocked);
        return rval;
    }

    bool GetValueAsBool( int row, int col ) {
        return (bool)GetValueAsLong(row, col);
    }

    void SetValueAsLong( int row, int col, long value ) {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "SetValue")) {
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iii)", row, col, value));
        }
        wxPyEndBlockThreads(blocked);
    }

    void SetValueAsDouble( int row, int col, double value ) {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if (wxPyCBH_findCallback(m_myInst, "SetValue")) {
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iid)", row, col, value));
        }
        wxPyEndBlockThreads(blocked);
    }

    void SetValueAsBool( int row, int col, bool value ) {
        SetValueAsLong( row, col, (long)value );
    }


    PYPRIVATE;
};
%}


// The python-aware version get's SWIGified
class wxPySheetTableBase : public wxSheetTable
{
public:
	%pythonAppend wxPySheetTableBase "self._setCallbackInfo(self, PySheetTableBase)"
    wxPySheetTableBase();
    void _setCallbackInfo(PyObject* self, PyObject* _class);

    %extend { void Destroy() { delete self; } }

    wxString base_GetTypeName( wxSheetCoords coords );
    bool base_CanGetValueAs( wxSheetCoords coords, const wxString& typeName );
    bool base_CanSetValueAs( wxSheetCoords coords, const wxString& typeName );
/*    
    bool base_InsertRows( size_t pos = 0, size_t numRows = 1 );
    bool base_AppendRows( size_t numRows = 1 );
    bool base_DeleteRows( size_t pos = 0, size_t numRows = 1 );
    bool base_InsertCols( size_t pos = 0, size_t numCols = 1 );
    bool base_AppendCols( size_t numCols = 1 );
    bool base_DeleteCols( size_t pos = 0, size_t numCols = 1 );
*/
    
//    bool base_CanHaveAttributes();
    wxSheetCellAttr base_GetAttr( const wxSheetCoords& coords, 
                                       wxSheetAttr_Type kind );
    void base_SetAttr(const wxSheetCoords& coords, 
                            const wxSheetCellAttr& attr, wxSheetAttr_Type kind);
//    void base_SetRowAttr(wxSheetCellAttr *attr, int row);
//    void base_SetColAttr(wxSheetCellAttr *attr, int col);
};


class wxSheetBlock
{
public:    
    wxSheetBlock();
    wxSheetBlock(int row, int col, int height, int width);
    wxSheetBlock( const wxSheetCoords& coords1, 
                  const wxSheetCoords& coords2, bool make_upright = true );
    wxSheetBlock( const wxSheetCoords& tl, int height, int width ); 

    int GetLeft()   const;
    int GetRight()  const;
    int GetTop()    const;
    int GetBottom() const;
    int GetWidth()  const;
    int GetHeight() const;

    wxSheetCoords GetLeftTop()     const;
    wxSheetCoords GetLeftBottom()  const;
    wxSheetCoords GetRightTop()    const;
    wxSheetCoords GetRightBottom() const;
    
    wxSheetCoords GetSize() const;
    
    wxArraySheetCoords GetArrayCoords() const;
    
    void SetLeft( int left );
    void SetTop( int top );
    void SetRight( int right );
    void SetBottom( int bottom );
    void SetWidth( int width );
    void SetHeight( int height );
    
    void SetLeftTop(const wxSheetCoords& lt);
    void SetLeftBottom(const wxSheetCoords& lb);
    void SetRightTop(const wxSheetCoords& rt);
    void SetRightBottom(const wxSheetCoords& rb);

    void SetLeftCoord( int left );
    void SetTopCoord( int top );
    void SetRightCoord( int right );
    void SetBottomCoord( int bottom );

    void SetLeftTopCoords(const wxSheetCoords& lt);
    void SetLeftBottomCoords(const wxSheetCoords& lb);
    void SetRightTopCoords(const wxSheetCoords& rt);
    void SetRightBottomCoords(const wxSheetCoords& rb);
    
    void Set( int row, int col, int height, int width );
    void SetCoords( int top, int left, int bottom, int right );
    void SetSize(const wxSheetCoords& size) { m_height = size.m_row; m_width = size.m_col; }
    
    // Get a block of this that is upright
    wxSheetBlock GetAligned() const;
    
    bool IsEmpty() const;
    bool IsOneCell() const;
    
    bool Contains( int row, int col ) const;
    bool Contains( const wxSheetCoords &coord ) const;
    bool Contains( const wxSheetBlock &b ) const;
    bool Intersects( const wxSheetBlock &b ) const;
    wxSheetBlock Intersect( const wxSheetBlock &other ) const;

    wxSheetBlock Union( const wxSheetBlock &other ) const;
    
    wxSheetBlock ExpandUnion( const wxSheetBlock &other ) const;
    
    bool Touches(const wxSheetBlock &block) const;
        
    int SideMatches(const wxSheetBlock& block) const;
    
    bool Combine(const wxSheetBlock &block);
                 
    int Combine( const wxSheetBlock &block, 
                  wxSheetBlock &top, wxSheetBlock &bottom, 
                  wxSheetBlock &left, wxSheetBlock &right ) const;

    int Delete( const wxSheetBlock &block, 
                 wxSheetBlock &top,  wxSheetBlock &bottom, 
                 wxSheetBlock &left, wxSheetBlock &right ) const;

    bool UpdateRows( size_t row, int numRows );
    bool UpdateCols( size_t col, int numCols );

    // operators
    bool operator == (const wxSheetBlock& b) const;
    bool operator != (const wxSheetBlock& b) const;

    int CmpTopLeft(const wxSheetBlock& b) const; 
    int CmpBottomRight(const wxSheetBlock& b) const;

    bool operator <  (const wxSheetBlock& b) const; 
    bool operator <= (const wxSheetBlock& other) const;
    bool operator >  (const wxSheetBlock& other) const;
    bool operator >= (const wxSheetBlock& other) const;
    
};

class wxSheetSelection : public wxObject
{
public:
    wxSheetSelection( int options = wxSHEET_SELECTION_NONE );
    wxSheetSelection( const wxSheetSelection& other );
    wxSheetSelection( const wxSheetBlock& block, 
                      int options = wxSHEET_SELECTION_NONE );
    
    void Copy(const wxSheetSelection &source);

    int GetNumberRows() const;
    int GetNumberCols() const;

    int GetOptions() const;
    void SetOptions(int options);
    
    bool HasSelection() const;
    int  GetCount() const;
    bool IsMinimzed() const;
    
    bool Clear(); 
    bool Empty(); 

    const wxArraySheetBlock& GetBlockArray() const;

    const wxSheetBlock& GetBlock( size_t index ) const;
    const wxSheetBlock& Item( size_t index ) const;
    
    const wxSheetBlock& GetBoundingBlock() const;
    void SetBoundingBlock(const wxSheetBlock& block);
    
    bool Contains( int row, int col ) const;
    bool Contains( const wxSheetCoords &c ) const;
    bool Contains( const wxSheetBlock &b ) const;

    int Index( int row, int col ) const;
    int Index( const wxSheetCoords &c ) const;
    int Index( const wxSheetBlock &b ) const;
    int IndexIntersects( const wxSheetBlock &b ) const;
    
    bool SelectBlock( const wxSheetBlock &block, bool combine_now = true, 
                      wxArraySheetBlock *addedBlocks = NULL );    
    bool DeselectBlock( const wxSheetBlock &block, bool combine_now = true,
                        wxArraySheetBlock *deletedBlocks = NULL );

    bool UpdateRows( size_t row, int numRows );
    bool UpdateCols( size_t col, int numCols );

    int IndexForInsert(const wxSheetBlock& block) const;
    int FindTopRow(int row) const;
    bool Minimize();
};

%constant wxEventType wxEVT_SHEET_VIEW_CHANGED;
%constant wxEventType wxEVT_SHEET_SELECTING_CELL;
%constant wxEventType wxEVT_SHEET_SELECTED_CELL;
%constant wxEventType wxEVT_SHEET_CELL_LEFT_DOWN;
%constant wxEventType wxEVT_SHEET_CELL_RIGHT_DOWN;
%constant wxEventType wxEVT_SHEET_CELL_LEFT_UP;
%constant wxEventType wxEVT_SHEET_CELL_RIGHT_UP;
%constant wxEventType wxEVT_SHEET_CELL_LEFT_DCLICK;
%constant wxEventType wxEVT_SHEET_CELL_RIGHT_DCLICK;
%constant wxEventType wxEVT_SHEET_LABEL_LEFT_DOWN;
%constant wxEventType wxEVT_SHEET_LABEL_RIGHT_DOWN;
%constant wxEventType wxEVT_SHEET_LABEL_LEFT_UP;
%constant wxEventType wxEVT_SHEET_LABEL_RIGHT_UP;
%constant wxEventType wxEVT_SHEET_LABEL_LEFT_DCLICK;
%constant wxEventType wxEVT_SHEET_LABEL_RIGHT_DCLICK;
%constant wxEventType wxEVT_SHEET_ROW_SIZE;
%constant wxEventType wxEVT_SHEET_ROW_SIZING;
%constant wxEventType wxEVT_SHEET_ROW_SIZED;
%constant wxEventType wxEVT_SHEET_COL_SIZE;
%constant wxEventType wxEVT_SHEET_COL_SIZING;
%constant wxEventType wxEVT_SHEET_COL_SIZED;
%constant wxEventType wxEVT_SHEET_RANGE_SELECTING;
%constant wxEventType wxEVT_SHEET_RANGE_SELECTED;
%constant wxEventType wxEVT_SHEET_CELL_VALUE_CHANGING;
%constant wxEventType wxEVT_SHEET_CELL_VALUE_CHANGED;
%constant wxEventType wxEVT_SHEET_EDITOR_ENABLED;
%constant wxEventType wxEVT_SHEET_EDITOR_DISABLED;
%constant wxEventType wxEVT_SHEET_EDITOR_CREATED;




%pythoncode {
EVT_SHEET_VIEW_CHANGED        = wx.PyEventBinder( wxEVT_SHEET_VIEW_CHANGED)
EVT_SHEET_SELECTING_CELL      = wx.PyEventBinder( wxEVT_SHEET_SELECTING_CELL)
EVT_SHEET_SELECTED_CELL       = wx.PyEventBinder( wxEVT_SHEET_SELECTED_CELL)
EVT_SHEET_CELL_LEFT_DOWN      = wx.PyEventBinder( wxEVT_SHEET_CELL_LEFT_DOWN)
EVT_SHEET_CELL_RIGHT_DOWN     = wx.PyEventBinder( wxEVT_SHEET_CELL_RIGHT_DOWN)
EVT_SHEET_CELL_LEFT_UP        = wx.PyEventBinder( wxEVT_SHEET_CELL_LEFT_UP)
EVT_SHEET_CELL_RIGHT_UP       = wx.PyEventBinder( wxEVT_SHEET_CELL_RIGHT_UP)
EVT_SHEET_CELL_LEFT_DCLICK    = wx.PyEventBinder( wxEVT_SHEET_CELL_LEFT_DCLICK)
EVT_SHEET_CELL_RIGHT_DCLICK   = wx.PyEventBinder( wxEVT_SHEET_CELL_RIGHT_DCLICK)
EVT_SHEET_LABEL_LEFT_DOWN     = wx.PyEventBinder( wxEVT_SHEET_LABEL_LEFT_DOWN)
EVT_SHEET_LABEL_RIGHT_DOWN    = wx.PyEventBinder( wxEVT_SHEET_LABEL_RIGHT_DOWN)
EVT_SHEET_LABEL_LEFT_UP       = wx.PyEventBinder( wxEVT_SHEET_LABEL_LEFT_UP)
EVT_SHEET_LABEL_RIGHT_UP      = wx.PyEventBinder( wxEVT_SHEET_LABEL_RIGHT_UP)
EVT_SHEET_LABEL_LEFT_DCLICK   = wx.PyEventBinder( wxEVT_SHEET_LABEL_LEFT_DCLICK)
EVT_SHEET_LABEL_RIGHT_DCLICK  = wx.PyEventBinder( wxEVT_SHEET_LABEL_RIGHT_DCLICK)
EVT_SHEET_ROW_SIZE            = wx.PyEventBinder( wxEVT_SHEET_ROW_SIZE)
EVT_SHEET_ROW_SIZING          = wx.PyEventBinder( wxEVT_SHEET_ROW_SIZING)
EVT_SHEET_ROW_SIZED           = wx.PyEventBinder( wxEVT_SHEET_ROW_SIZED)
EVT_SHEET_COL_SIZE            = wx.PyEventBinder( wxEVT_SHEET_COL_SIZE)
EVT_SHEET_COL_SIZING          = wx.PyEventBinder( wxEVT_SHEET_COL_SIZING)
EVT_SHEET_COL_SIZED           = wx.PyEventBinder( wxEVT_SHEET_COL_SIZED)
EVT_SHEET_RANGE_SELECTING     = wx.PyEventBinder( wxEVT_SHEET_RANGE_SELECTING)
EVT_SHEET_RANGE_SELECTED      = wx.PyEventBinder( wxEVT_SHEET_RANGE_SELECTED)
EVT_SHEET_CELL_VALUE_CHANGING = wx.PyEventBinder( wxEVT_SHEET_CELL_VALUE_CHANGING)
EVT_SHEET_CELL_VALUE_CHANGED  = wx.PyEventBinder( wxEVT_SHEET_CELL_VALUE_CHANGED)
EVT_SHEET_EDITOR_ENABLED      = wx.PyEventBinder( wxEVT_SHEET_EDITOR_ENABLED)
EVT_SHEET_EDITOR_DISABLED     = wx.PyEventBinder( wxEVT_SHEET_EDITOR_DISABLED)
EVT_SHEET_EDITOR_CREATED      = wx.PyEventBinder( wxEVT_SHEET_EDITOR_CREATED)


%# The same as above but with the ability to specify an identifier

EVT_SHEET_CMD_VIEW_CHANGED        = wx.PyEventBinder( wxEVT_SHEET_VIEW_CHANGED,        1 )
EVT_SHEET_CMD_SELECTING_CELL      = wx.PyEventBinder( wxEVT_SHEET_SELECTING_CELL,      1 )
EVT_SHEET_CMD_SELECTED_CELL       = wx.PyEventBinder( wxEVT_SHEET_SELECTED_CELL,       1 )
EVT_SHEET_CMD_CELL_LEFT_DOWN      = wx.PyEventBinder( wxEVT_SHEET_CELL_LEFT_DOWN,      1 )
EVT_SHEET_CMD_CELL_RIGHT_DOWN     = wx.PyEventBinder( wxEVT_SHEET_CELL_RIGHT_DOWN,     1 )
EVT_SHEET_CMD_CELL_LEFT_UP        = wx.PyEventBinder( wxEVT_SHEET_CELL_LEFT_UP,        1 )
EVT_SHEET_CMD_CELL_RIGHT_UP       = wx.PyEventBinder( wxEVT_SHEET_CELL_RIGHT_UP,       1 )
EVT_SHEET_CMD_CELL_LEFT_DCLICK    = wx.PyEventBinder( wxEVT_SHEET_CELL_LEFT_DCLICK,    1 )
EVT_SHEET_CMD_CELL_RIGHT_DCLICK   = wx.PyEventBinder( wxEVT_SHEET_CELL_RIGHT_DCLICK,   1 )
EVT_SHEET_CMD_LABEL_LEFT_DOWN     = wx.PyEventBinder( wxEVT_SHEET_LABEL_LEFT_DOWN,     1 )
EVT_SHEET_CMD_LABEL_RIGHT_DOWN    = wx.PyEventBinder( wxEVT_SHEET_LABEL_RIGHT_DOWN,    1 )
EVT_SHEET_CMD_LABEL_LEFT_UP       = wx.PyEventBinder( wxEVT_SHEET_LABEL_LEFT_UP,       1 )
EVT_SHEET_CMD_LABEL_RIGHT_UP      = wx.PyEventBinder( wxEVT_SHEET_LABEL_RIGHT_UP,      1 )
EVT_SHEET_CMD_LABEL_LEFT_DCLICK   = wx.PyEventBinder( wxEVT_SHEET_LABEL_LEFT_DCLICK,   1 )
EVT_SHEET_CMD_LABEL_RIGHT_DCLICK  = wx.PyEventBinder( wxEVT_SHEET_LABEL_RIGHT_DCLICK,  1 )
EVT_SHEET_CMD_ROW_SIZE            = wx.PyEventBinder( wxEVT_SHEET_ROW_SIZE,    1 )
EVT_SHEET_CMD_ROW_SIZING          = wx.PyEventBinder( wxEVT_SHEET_ROW_SIZING,  1 )
EVT_SHEET_CMD_ROW_SIZED           = wx.PyEventBinder( wxEVT_SHEET_ROW_SIZED,   1 )
EVT_SHEET_CMD_COL_SIZE            = wx.PyEventBinder( wxEVT_SHEET_COL_SIZE,    1 )
EVT_SHEET_CMD_COL_SIZING          = wx.PyEventBinder( wxEVT_SHEET_COL_SIZING,  1 )
EVT_SHEET_CMD_COL_SIZED           = wx.PyEventBinder( wxEVT_SHEET_COL_SIZED,   1 )
EVT_SHEET_CMD_RANGE_SELECTING     = wx.PyEventBinder( wxEVT_SHEET_RANGE_SELECTING, 1 )
EVT_SHEET_CMD_RANGE_SELECTED      = wx.PyEventBinder( wxEVT_SHEET_RANGE_SELECTED,  1 )
EVT_SHEET_CMD_CELL_VALUE_CHANGING = wx.PyEventBinder( wxEVT_SHEET_CELL_VALUE_CHANGING,  1 )
EVT_SHEET_CMD_CELL_VALUE_CHANGED  = wx.PyEventBinder( wxEVT_SHEET_CELL_VALUE_CHANGED,   1 )
EVT_SHEET_CMD_EDITOR_ENABLED      = wx.PyEventBinder( wxEVT_SHEET_EDITOR_ENABLED,       1 )
EVT_SHEET_CMD_EDITOR_DISABLED     = wx.PyEventBinder( wxEVT_SHEET_EDITOR_DISABLED,      1 )
EVT_SHEET_CMD_EDITOR_CREATED      = wx.PyEventBinder( wxEVT_SHEET_EDITOR_CREATED, 1 )

}

//---------------------------------------------------------------------------

%init %{
%}

//---------------------------------------------------------------------------
//---------------------------------------------------------------------------
