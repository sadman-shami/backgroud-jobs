import React, { useEffect, useState } from "react";

import { ScrollArea } from "@/components/ui/scroll-area";
import { useWebsocket } from "@/WebSocket";

const Logging: React.FC = () => {
  const { ws } = useWebsocket();
  const [log, setLog] = useState<string[]>([]);

  const listenTask = (e: MessageEvent) => {
    const wsresponse = JSON.parse(e.data) as {
      type: string;
      payload: string;
    };
    if (wsresponse.type === "logging") {
      const payload = wsresponse.payload;
      setLog((prev) => [...prev, payload]);
    }
  };

  useEffect(() => {
    ws?.addEventListener("message", listenTask);
    return () => ws?.removeEventListener("message", listenTask);
  }, [ws]);

  return (
    <div>
      <h1 className="my-4 text-xl font-bold">Background Job Logs</h1>
      {log.length > 0 && (
        <ScrollArea
          className={
            "h-100 py-2 border border-accent rounded-md bg-accent p-2 text-sm"
          }
        >
          <ul>
            {log.map((item, i) => (
              <li key={i} className="text-bold">
                {item}
              </li>
            ))}
          </ul>
        </ScrollArea>
      )}
    </div>
  );
};

export default Logging;
