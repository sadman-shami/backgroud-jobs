import axios from "axios";
import React, { useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Spinner } from "@/components/ui/spinner";
import { useWebsocket } from "@/WebSocket";
import { Trash } from "lucide-react";

interface ITask {
  id: string;
  expression: string;
  result: string;
  status: "DONE" | "PROCESSING" | "FAILED";
  created_at: string;
}

export const beautifyTime = (datetime: string) =>
  new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(datetime));

const Task: React.FC<{ task: ITask }> = ({ task }) => {
  const [loading, setLoading] = useState<boolean>(false);

  const deleteTask = async () => {
    if (task.status !== "PROCESSING") {
      setLoading(true);
      await axios.delete(`http://127.0.0.1:8000/task/${task.id}`);
      setLoading(false);
    }
  };

  return (
    <div className="border border-accent rounded-md p-2 mb-2 text-sm flex justify-between">
      <div className="flex flex-col gap-y-2">
        <h1>Expression: {task.expression}</h1>
        <div className="flex items-center gap-x-2">
          <p>Status: </p>
          <Badge
            variant={"outline"}
            className="flex justify-around items-center p-3"
          >
            {task.status !== "PROCESSING" && (
              <div
                className={`w-2 h-2 ${task.status === "DONE" ? "bg-green-500" : "bg-red-500"} rounded-full`}
              ></div>
            )}
            {task.status === "PROCESSING" && <Spinner />}
            <p>{task.status}</p>
          </Badge>
        </div>
        <p>Result: {task.result ?? "Result not found"}</p>
        <p>Task Created: {beautifyTime(task.created_at)}</p>
      </div>
      <Button
        variant={"destructive"}
        size={"icon-sm"}
        className={"cursor-pointer"}
        disabled={task.status === "PROCESSING" || loading}
        onClick={deleteTask}
      >
        {loading ? <Spinner /> : <Trash />}
      </Button>
    </div>
  );
};

const TasksView: React.FC = () => {
  const { ws } = useWebsocket();
  const [processedTask, setProcessedTask] = useState<ITask[]>([]);
  const [doneTask, setDoneTask] = useState<ITask[]>([]);

  const listenTask = (e: MessageEvent) => {
    const payload = (JSON.parse(e.data) as { type: string; payload: string[] })
      .payload;
    setDoneTask([]);
    setProcessedTask([]);
    const tasks: ITask[] = [];
    payload.map((item) => {
      tasks.push(JSON.parse(item) as ITask);
    });
    const pt = tasks.filter((task) => task.status === "PROCESSING");
    const dt = tasks.filter((task) => task.status !== "PROCESSING");
    setDoneTask(dt);
    setProcessedTask(pt);
  };

  useEffect(() => {
    ws?.addEventListener("message", listenTask);
    return () => ws?.removeEventListener("message", listenTask);
  }, [ws]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <h1 className="my-4 text-xl border-b font-bold">Done/Failed Jobs</h1>
        {doneTask.length > 0 && (
          <ScrollArea className={"h-125 py-2"}>
            {doneTask.map((task) => (
              <Task task={task} key={task.id} />
            ))}
          </ScrollArea>
        )}
      </div>
      <div>
        <h1 className="my-4 text-xl border-b font-bold">Background Jobs</h1>
        {processedTask.length > 0 && (
          <ScrollArea className={"h-125 py-2"}>
            {processedTask.map((task) => (
              <Task task={task} key={task.id} />
            ))}
          </ScrollArea>
        )}
      </div>
    </div>
  );
};

export default TasksView;
