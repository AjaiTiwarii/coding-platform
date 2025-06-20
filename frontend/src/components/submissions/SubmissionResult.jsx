import { useParams } from 'react-router-dom'
import { useApi } from '../../hooks/useApi'
import { Loader } from '../common/UI/Loader'
import { Alert } from '../common/UI/Alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../common/UI/Tabs'

export const SubmissionResult = () => {
  const { id } = useParams()
  const { data: submission, loading, error, get } = useApi()

  useEffect(() => {
    const fetchSubmission = async () => {
      await get(`/submissions/${id}/`)
    }
    fetchSubmission()
  }, [id])

  return (
    <div className="space-y-6">
      {loading && <Loader />}
      
      {error && (
        <Alert type="error">Failed to load submission: {error.message}</Alert>
      )}

      {!loading && !error && submission && (
        <>
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-2xl font-bold mb-4">Submission Details</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm text-gray-600">Problem</label>
                <p className="font-medium">{submission.problem.title}</p>
              </div>
              <div>
                <label className="text-sm text-gray-600">Language</label>
                <p className="font-medium">{submission.language.name}</p>
              </div>
              <div>
                <label className="text-sm text-gray-600">Status</label>
                <p className={getStatusColor(submission.status)}>
                  {submission.status}
                </p>
              </div>
              <div>
                <label className="text-sm text-gray-600">Score</label>
                <p className="font-medium">{submission.score}%</p>
              </div>
            </div>
          </div>

          <Tabs defaultValue="testcases">
            <TabsList>
              <TabsTrigger value="testcases">Test Cases</TabsTrigger>
              <TabsTrigger value="code">Code</TabsTrigger>
            </TabsList>

            <TabsContent value="testcases">
              <div className="bg-white p-6 rounded-lg shadow-sm space-y-4">
                {submission.test_results?.map((result, index) => (
                  <div 
                    key={result.id}
                    className={`p-4 rounded-md border ${
                      result.status === 'ACCEPTED' 
                        ? 'border-green-100 bg-green-50' 
                        : 'border-red-100 bg-red-50'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">Test Case #{index + 1}</span>
                      <span className={`text-sm ${result.status === 'ACCEPTED' ? 'text-green-700' : 'text-red-700'}`}>
                        {result.status}
                      </span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                      <div>
                        <label className="text-gray-600">Input</label>
                        <pre className="whitespace-pre-wrap">{result.test_case.input_data}</pre>
                      </div>
                      <div>
                        <label className="text-gray-600">Expected</label>
                        <pre className="whitespace-pre-wrap">{result.test_case.expected_output}</pre>
                      </div>
                      <div>
                        <label className="text-gray-600">Actual</label>
                        <pre className="whitespace-pre-wrap">{result.output}</pre>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="code">
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <pre className="p-4 bg-gray-50 rounded-md overflow-x-auto">
                  {submission.code}
                </pre>
              </div>
            </TabsContent>
          </Tabs>
        </>
      )}
    </div>
  )
}
