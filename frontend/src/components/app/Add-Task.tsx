import axios from "axios";
import React, { useState } from "react";

import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Spinner } from "@/components/ui/spinner";
import { Textarea } from "@/components/ui/textarea";

const AddTask: React.FC = () => {
  const [expression, setExpression] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const addTask = async () => {
    if (expression.length == 0) {
      alert("Expression must 1 character");
    } else {
      setLoading(true);
      await axios.post("http://127.0.0.1:8000/task", {
        expression,
      });
      setLoading(false);
      setExpression("");
    }
  };

  return (
    <div>
      <Label htmlFor="task-expression" className="mb-2">
        Mathemetical expression for task
      </Label>
      <Textarea
        id="task-expression"
        placeholder="Mathematical Expression: i.e. (12*242)+89"
        autoComplete="off"
        className="max-w-125 resize-y"
        value={expression}
        onChange={(e) => setExpression(e.target.value)}
      />
      <Button className="mt-2" disabled={loading} onClick={addTask}>
        Add Task {loading && <Spinner />}{" "}
      </Button>
    </div>
  );
};

export default AddTask;
