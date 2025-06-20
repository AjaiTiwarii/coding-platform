const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200">
      <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <p className="text-gray-600 text-sm">
            &copy; {new Date().getFullYear()} CodeMaster. All rights reserved.
          </p>
          <div className="flex space-x-4">
            <a href="/terms" className="text-gray-600 hover:text-gray-900 text-sm">
              Terms
            </a>
            <a href="/privacy" className="text-gray-600 hover:text-gray-900 text-sm">
              Privacy
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer;
