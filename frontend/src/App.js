import React, { useState } from "react";
import axios from "axios";

function App() {
  const [issue, setIssue] = useState("");
  const [loading, setLoading] = useState(false);
  const [initial, setInitial] = useState(true);
  const [response, setResponse] = useState("");

  async function handlePost(value) {
    setInitial(false);
    setLoading(true);

    axios.post("http://127.0.0.1:5000/api", { 'issue': value })
      .then((res) => {
        setLoading(false);
        setResponse(res.data)
      })
      .catch((err) => {
        setLoading(false);
        console.log(err);
      })
  }

  return (
    <div className='flex flex-col px-24'>
      <div className='flex flex-row items-center w-full'>
        <div className="w-1/6">
          <img src={'https://www.societegenerale.com/sites/default/files/logo-societe-generale.png'} className='w-32' />
        </div>
        <div className="w-5/6 flex flex-col items-center">
          <p className='text-3xl font-semibold w-full text-center'>IDENTIFICATION OF POTENTIAL HOTSPOTS IN NETWORK INFRASTRUCTURE</p>
          <div className="w-[70%] h-1 rounded-full bg-red-500 mt-1"></div>
        </div>
      </div>

      <div className='flex flex-row items-center gap-12 mt-8'>
        <p className="font-semibold text-xl w-1/6">Describe your issue</p>
        <textarea
          className="w-5/6 h-20 border-2 border-black rounded-xl px-4 py-2"
          name="textValue"
          onChange={(e) => {
            setIssue(e.target.value);
          }}
          placeholder="Eg. Users are experiencing slow access to online resources due to network congestion during peak hours."
        />
      </div>

      <div className="w-full flex justify-end mt-8">
        <button
          onClick={() => { handlePost(issue) }}
          className='w-fit px-4 py-2 bg-black text-white text-lg rounded-lg'
        >
          Resolve
        </button>
      </div>

      {!initial && (
        loading ? (
          <div className="flex flex-row gap-12 mt-24 animate-pulse w-full">
            <div className="flex flex-col gap-2 w-1/6">
              <div className="bg-gray-200 w-5/6 h-8 rounded-lg"></div>
              <div className="bg-gray-200 w-3/4 h-6 rounded-md"></div>
            </div>

            <div className="flex flex-col gap-2 w-5/6">
              <div className="bg-gray-200 w-full h-10 rounded-xl"></div>
              <div className="bg-gray-200 w-5/6 h-8 rounded-lg"></div>
              <div className="bg-gray-200 w-3/4 h-6 rounded-md"></div>
            </div>
          </div>
        ) : (
          <div className="flex flex-row gap-12 mt-24 w-full">
            <p className="font-semibold text-xl w-1/6">Resolution</p>

            <p className="text-lg w-5/6">{response}</p>
          </div>
        )
      )}
    </div>
  );
}

export default App;
