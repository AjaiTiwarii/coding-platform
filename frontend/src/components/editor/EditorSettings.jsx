import { Slider } from '../common/UI/Slider'
import { Select } from '../common/UI/Select'

export const EditorSettings = ({
  theme,
  fontSize,
  tabSize,
  onThemeChange,
  onFontSizeChange,
  onTabSizeChange
}) => {
  const themes = [
    { value: 'vs-dark', label: 'Dark' },
    { value: 'vs-light', label: 'Light' },
    { value: 'hc-black', label: 'High Contrast' }
  ]

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Select
          label="Theme"
          value={theme}
          options={themes}
          onChange={onThemeChange}
        />
        
        <Slider
          label="Font Size"
          min="12"
          max="24"
          value={fontSize}
          onChange={onFontSizeChange}
        />
        
        <Slider
          label="Tab Size"
          min="2"
          max="8"
          step="2"
          value={tabSize}
          onChange={onTabSizeChange}
        />
      </div>
    </div>
  )
}
