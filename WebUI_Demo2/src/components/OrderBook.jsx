import { useEffect, useState } from "react";

export default function OrderBook() {
  const [bids, setBids] = useState([]);
  const [asks, setAsks] = useState([]);
  const [price, setPrice] = useState(0);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/book");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setBids(data.bids);
      setAsks(data.asks);
      setPrice(data.last_price);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="grid grid-cols-2 gap-12">
      <div className="col-span-2 text-center mb-8">
        <div className="text-4xl font-bold">
          Market Price:{" "}
          <span className="text-yellow-400">
            {price ? price.toFixed(2) : "—"}
          </span>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-green-400 mb-2">Bids</h2>
        <table className="w-full">
          <thead>
            <tr className="text-gray-400 border-b border-gray-700">
              <th className="py-2">Price</th>
              <th>Qty</th>
            </tr>
          </thead>
          <tbody>
            {bids.map(([p, q], idx) => (
              <tr key={idx} className="border-b border-gray-800">
                <td className="py-1 text-green-300">{p}</td>
                <td className="py-1">{q}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-red-400 mb-2">Asks</h2>
        <table className="w-full">
          <thead>
            <tr className="text-gray-400 border-b border-gray-700">
              <th className="py-2">Price</th>
              <th>Qty</th>
            </tr>
          </thead>
          <tbody>
            {asks.map(([p, q], idx) => (
              <tr key={idx} className="border-b border-gray-800">
                <td className="py-1 text-red-300">{p}</td>
                <td className="py-1">{q}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
