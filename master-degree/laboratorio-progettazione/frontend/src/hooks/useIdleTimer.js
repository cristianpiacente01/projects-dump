import { useEffect, useRef, useCallback } from "react";

const useIdleTimer = (
  onTimeout,
  onWarning,
  enabled = true,
  warningTime = 30,
  timeout = 600
) => {
  const lastActivityRef = useRef(Date.now());
  const hasWarnedRef = useRef(false);
  const intervalRef = useRef(null);

  const resetTimer = useCallback(() => {
    // Manual reset
    lastActivityRef.current = Date.now();
    hasWarnedRef.current = false;
  }, []);

  useEffect(() => {
    if (!enabled) return;

    const updateActivity = () => {
      if (!hasWarnedRef.current) {
        lastActivityRef.current = Date.now();
      } // else ignore activity after warning
    };

    const events = ["mousemove", "keydown", "click"];
    events.forEach((e) => window.addEventListener(e, updateActivity));

    intervalRef.current = setInterval(() => {
      const now = Date.now();
      const idleSeconds = (now - lastActivityRef.current) / 1000;

      if (!hasWarnedRef.current && idleSeconds >= timeout - warningTime) {
        hasWarnedRef.current = true;
        // Warning triggered
        onWarning();
      }

      if (idleSeconds >= timeout) {
        // Auto logout
        onTimeout();
      }
    }, 1000);

    return () => {
      clearInterval(intervalRef.current);
      events.forEach((e) => window.removeEventListener(e, updateActivity));
    };
  }, [enabled, onTimeout, onWarning, warningTime, timeout]);

  return { resetTimer, warningTime };
};

export default useIdleTimer;
