import React from "react";

interface NumberFieldProps {
  label?: string;
  value: number;
  onChange: (value: number) => void;
  className?: string;
  min?: number;
  max?: number;
  step?: number;
}

export const NumberField: React.FC<NumberFieldProps> = ({
  label ="",
  value,
  onChange,
  className = "",
  min,
  max,
  step,
}) => {

  return (
    <div className={`flex flex-col gap-1 ${className}`}>
      <label className="font-semibold text-sm">
        {label}
      </label>
      <input
        type="number"
        value={Number.isNaN(value) ? "" : value}
        min={min}
        max={max}
        step={step}
        onChange={(e) => {
          const val = e.target.value;
          onChange(val === "" ? 0 : Number(val));
        }}
        className="p-2 bg-ctp-crust  text-sm focus:outline-none transition-colors"
      />
    </div>
  );
};