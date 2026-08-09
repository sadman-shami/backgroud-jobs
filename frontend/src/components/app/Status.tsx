import React, { useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { useWebsocket } from "@/WebSocket";

const Status: React.FC = () => {
  const { ws } = useWebsocket();
  const [connected, setConnected] = useState<boolean>(false);
  useEffect(() => {
    ws?.addEventListener("open", (_) => {
      setConnected(true);
    });
    ws?.addEventListener("close", (_) => {
      setConnected(false);
    });
    return () => {
      ws?.removeEventListener("open", (_) => {
        setConnected(true);
      });
      ws?.removeEventListener("close", (_) => {
        setConnected(false);
      });
    };
  }, [ws]);
  return (
    <Badge variant={"outline"} className="flex justify-around items-center p-3">
      <div
        className={`w-2 h-2 ${connected ? "bg-green-500" : "bg-red-500"} rounded-full animate-pulse`}
      ></div>
      <p>{connected ? "Connected" : "Disconnected"}</p>
    </Badge>
  );
};

export default Status;
