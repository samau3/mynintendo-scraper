const API_STATUS_URL = "https://j50pzswk.status.cron-job.org/";

interface ErrorViewProps {
  errorInfo: string;
}

export default function ErrorView({ errorInfo }: ErrorViewProps) {
  return (
    <div className="text-center">
      <p className="text-lg font-bold text-red-700">{errorInfo}</p>
      <p className="text-lg font-bold dark:text-gray-300">
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
      <button className="m-2 rounded-lg bg-blue-100 p-2 text-sm font-bold uppercase text-blue-600">
        <a href={API_STATUS_URL} target="_blank">
          API Status
        </a>
      </button>
    </div>
  );
}
