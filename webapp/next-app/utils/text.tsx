import React from "react";

export function nl2br(text: string) {
  return text.split('\n').map((item, key) => {
    return <React.Fragment key={key}>{item}<br/></React.Fragment>
  })
}
