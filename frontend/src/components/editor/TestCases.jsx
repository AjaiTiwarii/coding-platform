import { Tabs, TabsContent, TabsList, TabsTrigger } from '../common/UI/Tabs'

export const TestCases = ({ testCases }) => {
  const sampleCases = testCases?.filter(tc => tc.is_sample) || []

  return (
    <div className="bg-white rounded-lg shadow-sm p-4">
      <h3 className="text-lg font-medium mb-4">Test Cases</h3>
      
      <Tabs defaultValue="sample" className="space-y-4">
        <TabsList>
          <TabsTrigger value="sample">Sample Cases</TabsTrigger>
          <TabsTrigger value="hidden" disabled>
            Hidden Cases
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="sample">
          <div className="space-y-4">
            {sampleCases.map((testCase, index) => (
              <div key={testCase.id} className="space-y-2">
                <div className="text-sm font-medium">
                  Case {index + 1} ({testCase.points} points)
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs text-gray-500">Input</label>
                    <pre className="bg-gray-50 p-2 rounded-md text-sm">
                      {testCase.input_data}
                    </pre>
                  </div>
                  <div>
                    <label className="text-xs text-gray-500">Expected Output</label>
                    <pre className="bg-gray-50 p-2 rounded-md text-sm">
                      {testCase.expected_output}
                    </pre>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
