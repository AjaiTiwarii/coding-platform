import { useSearchParams } from 'react-router-dom'
import { Select } from '@/components/common/UI/Select'
import { Input } from '@/components/common/UI/Input'


export const ProblemFilters = () => {
  const [searchParams, setSearchParams] = useSearchParams()

  const handleFilterChange = (name, value) => {
    const newParams = new URLSearchParams(searchParams)
    if (value) {
      newParams.set(name, value)
    } else {
      newParams.delete(name)
    }
    setSearchParams(newParams)
  }

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Input
          placeholder="Search problems..."
          value={searchParams.get('search') || ''}
          onChange={(e) => handleFilterChange('search', e.target.value)}
        />
        
        <Select
          value={searchParams.get('difficulty') || ''}
          onChange={(e) => handleFilterChange('difficulty', e.target.value)}
          options={[
            { value: '', label: 'All Difficulty' },
            { value: 'EASY', label: 'Easy' },
            { value: 'MEDIUM', label: 'Medium' },
            { value: 'HARD', label: 'Hard' }
          ]}
        />
        
        <Select
          value={searchParams.get('category') || ''}
          onChange={(e) => handleFilterChange('category', e.target.value)}
          options={[
            { value: '', label: 'All Categories' },
            { value: 'arrays', label: 'Arrays' },
            { value: 'strings', label: 'Strings' },
            { value: 'algorithms', label: 'Algorithms' }
          ]}
        />
      </div>
    </div>
  )
}
