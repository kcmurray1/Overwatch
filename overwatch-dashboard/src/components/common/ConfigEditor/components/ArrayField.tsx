import { observer } from "mobx-react-lite";
import { TextField } from "./TextField";
import { NumberField } from "./NumberField";

interface ArrayFieldProps {
    title: string;
    values: string[] | number[] | boolean[];
    className?: string
    onChange: (index: number, newValue: number | string | boolean) => void;
}

export const ArrayField = observer(({title, values, onChange}: ArrayFieldProps) => {
    return (
        <div>
            <h1 className="text-ctp-sapphire p-2">{title}</h1>
            <div className="grid grid-cols-5 gap-2 p-2">
             {values.map((value, index) => {
                    if (typeof value === "string") {
                        return <TextField
                            key={index}
                            label=""
                            value={value}
                            onChange={(value) => onChange(index, value)}
                            />
                    }
                    if (typeof value === "number") {
                        return <NumberField
                            key={index}
                            value={value}
                            onChange={(val) => onChange(index, val)}
                            />
                    }
                })}
            </div>
        </div>
    )
})