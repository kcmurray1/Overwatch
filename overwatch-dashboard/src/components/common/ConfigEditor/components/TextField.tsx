import React from "react";

interface TextFieldProps {
  label: string;
  value: string;
  onChange?: (value: string) => void;
  disabled?: boolean;
  placeholder?: string;
  className?: string;
}

export const TextField: React.FC<TextFieldProps> = ({
  label,
  value,
  onChange,
  disabled = false,
  placeholder = "",
  className = "",
}) => {

  return (
    <div className={`flex flex-col gap-1 ${className}`}>
      <label className="font-semibold text-sm">
        {label}
      </label>
      <input
        type="text"
        value={value ?? ""}
        disabled={disabled}
        placeholder={placeholder}
        onChange={(e) => onChange?.(e.target.value)}
        className={`p-2 transition-colors outline-none border focus:ring-1 focus:ring-blue-500 dark:focus:ring-amber-500 ${
          disabled
            ? "bg-gray-800/50  text-gray-500 cursor-not-allowed"
            : " "
        }`}
      />
    </div>
  );
};