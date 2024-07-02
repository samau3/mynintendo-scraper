const API_STATUS_URL = "https://j50pzswk.status.cron-job.org/";

interface IErrorViewProps {
  errorInfo: string
}

export default function ErrorView({ errorInfo } : IErrorViewProps) {
  return (
    <div className="text-center">
      <p className="font-bold text-lg text-red-700">{errorInfo}</p>
      <p className="font-bold text-lg dark:text-gray-300">
        Please create a new issue on the{" "}
        <a
          href={API_STATUS_URL}
          target="_blank"
          className="text-blue-600 underline"
        >
          Github repository
        </a>
        .
      </p>
      <button className="uppercase text-sm font-bold text-blue-600 p-2 m-2 bg-blue-100 rounded-lg">
        <a href={API_STATUS_URL} target="_blank">
          API Status
        </a>
      </button>
    </div>
  );
}
