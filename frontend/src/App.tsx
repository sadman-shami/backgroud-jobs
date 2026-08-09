import type React from "react";

import AddTask from "@/components/app/Add-Task";
import Logging from "@/components/app/Logging";
import Status from "@/components/app/Status";
import TasksView from "@/components/app/Tasks-View";
import { Separator } from "@/components/ui/separator";

const App: React.FC = () => {
  return (
    <div className="container mx-auto max-w-250 p-4">
      <div className="flex justify-between">
        <h1 className="text-2xl font-bold">Background Task</h1>
        <Status />
      </div>
      <Separator className={"my-8"} />
      <AddTask />
      <Separator className={"my-8"} />
      <TasksView />
      <Separator className={"my-8"} />
      <Logging />
    </div>
  );
};

export default App;
