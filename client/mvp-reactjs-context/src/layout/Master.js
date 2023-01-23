import Layouts from "./Layouts";
import { Outlet } from "react-router-dom";
import React from "react";

function MasterPage() {
  return (
    <>
      <Layouts>
        <Outlet /> {/* content from inside pages */}
      </Layouts>
    </>
  );
}

export default MasterPage;
