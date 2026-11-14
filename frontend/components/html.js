// Shared helper: `html` lets us write JSX-like templates without a build step.
import React from "react";
import htm from "htm";

export const html = htm.bind(React.createElement);
export { React };
