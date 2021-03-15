import vtk
class InteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, glyphs, renderer, data):
        self.glyphs = glyphs
        self.renderer = renderer
        self.data = data
        self.AddObserver("LeftButtonPressEvent", self._left_button_press_event)
        self._new_glyph_index = None
        self._old_glyph_index = None
        self._new_glyph_value = None    
        self._old_glyph_value = None

    def _left_button_press_event(self, obj, event):
        click_pos = self.GetInteractor().GetEventPosition()

        cell_picker = vtk.vtkCellPicker()
        cell_picker.Pick(click_pos[0], click_pos[1], 0, self.GetDefaultRenderer())
        if self._new_glyph_value:
            if self._old_glyph_value:
                self.data.GetPointData().GetArray('degree').SetValue(self._old_glyph_index, self._old_glyph_value)
        self._new_glyph_index = self.glyphs.GetOutput().GetPointData().GetArray("InputPointIds").GetValue(cell_picker.GetPointId())
        self._new_glyph_value = self.data.GetPointData().GetArray('degree').GetTuple1(self._new_glyph_index)
        self.data.GetPointData().GetArray('degree').SetValue(self._new_glyph_index, 20) 
        self._old_glyph_index = self._new_glyph_index
        self._old_glyph_value = self._new_glyph_value

        self.data.Modified()