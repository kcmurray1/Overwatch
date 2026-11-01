import { observer } from "mobx-react-lite";

interface BaseCardProps {
    children?: React.ReactNode
    className?: string
}

export const BaseCard = observer(({className, children}: BaseCardProps) => {
    return (
         <div className={`w-full p-4 flex-1 ${className}`}>
            {children}
        </div>
        
    )
})