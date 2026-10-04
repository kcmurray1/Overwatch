import { observer } from "mobx-react-lite";

interface BaseCardProps {
    children?: React.ReactNode
    className?: string
}

export const BaseCard = observer(({className, children}: BaseCardProps) => {
    return (
         <div className={`w-full rounded-lg p-4 bg-accent-light text-white dark:bg-primary-dark dark:text-fuchsia-100 ${className}`}>
            <input type="checkbox" id="select" name="selectCard" onClick={(e) => e.stopPropagation()}></input>
            {children}
        </div>
        
    )
})