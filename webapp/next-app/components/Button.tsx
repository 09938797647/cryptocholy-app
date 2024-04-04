import React from "react";


export enum ButtonType {
    primary = "primary",
    secondary = "secondary",
    disabled = "disabled",
}

export enum ButtonSize {
    s = "s",
    m = "m",
    l = "l",
}

export const LinkButton: React.FC<{
    title: string;
    link: string;
    type?: ButtonType;
    size?: ButtonSize;
}> = ({
          title,
          link,
          type,
          size,
      }) => {
    return (
        <_Button title={title} onButtonClick={null} link={link} isLoading={false} type={type} size={size}/>
    )
}

export const Button: React.FC<{
    isLoading: boolean;
    onButtonClick: React.MouseEventHandler<HTMLButtonElement>;
    title: string;
    type?: ButtonType;
    size?: ButtonSize;

}> = ({
          title,
          onButtonClick,
          isLoading,
          type,
          size,
      }) => {
    return (
        <_Button
            title={title}
            onButtonClick={onButtonClick}
            link={null}
            isLoading={isLoading}
            type={type}
            size={size}
        />
    )
}

const _Button: React.FC<{
    title: string;
    isLoading: boolean;
    link: string | null;
    onButtonClick: React.MouseEventHandler<HTMLButtonElement> | null;
    type?: ButtonType;
    size?: ButtonSize;
}> = (
    {
        title,
        isLoading = false,
        onButtonClick = null,
        link = null,
        type = ButtonType.primary,
        size = ButtonSize.m,
    }
) => {
    let classes = "font-normal transition block p-4 rounded-md mb-2 w-full border-2 text-left border-transparent-dark-30 hover:bg-transparent-dark-12 hover:dark:bg-transparent-light-12 dark:border-transparent-white-30"

    if (isLoading) {
        type = ButtonType.disabled
    }

    switch (size) {
        case ButtonSize.s:
            classes += " text-base p-3"
            break
        case ButtonSize.m:
            classes += " text-base p-4"
            break
        case ButtonSize.l:
            classes += " text-lg p-5"
            break
    }

    switch (type) {
        case ButtonType.primary:
            classes += " text-center bg-brand text-white border-brand"
            break
        case ButtonType.disabled:
            classes += " cursor-not-allowed opacity-50"
            break
    }

    if (onButtonClick) {
        return (
            <button onClick={!isLoading ? onButtonClick : null} className={classes}>
                {title}
            </button>
        )
    } else if (link) {
        return (
            <a href={link} className={classes}>{title}</a>
        )
    } else {
        return null
    }
}