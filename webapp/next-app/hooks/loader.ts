import { useState, useEffect } from 'react';

export const useLoader = (isLoading: boolean) => {
  const [renderLoader, setRenderLoader] = useState(false);

  useEffect(() => {
    let timer: any;
    if (isLoading) {
      timer = setTimeout(() => {
        setRenderLoader(true);
      }, 2000);
    } else {
      if (timer) {
        clearTimeout(timer);
      }
      setRenderLoader(false);
    }

    return () => {
      if (timer) {
        clearTimeout(timer);
      }
    };
  }, [isLoading]);

  return renderLoader;
};
