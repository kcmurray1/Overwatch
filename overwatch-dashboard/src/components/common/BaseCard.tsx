import { observer } from "mobx-react-lite";

interface BaseCardProps {
    children?: React.ReactNode
}

export const BaseCard = observer(({children}: BaseCardProps) => {
    return (
         <div className="rounded-lg p-4 bg-accent-light text-white dark:bg-primary-dark dark:text-fuchsia-100">
            <input type="checkbox" id="select" name="selectCard"></input>
            {children}
        </div>
        
    )
})