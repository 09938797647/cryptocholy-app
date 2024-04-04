import Image from "next/image";
import ReactMarkdown from "react-markdown";
import React from "react";
import { getImageUrl } from "../utils/image";


export const CardCenterWrapper: React.FC<{ children: any }> = ({children}) => {
    return (
        <div className="flex flex-col justify-center h-full">
            {children}
        </div>
    )

}

export const CardBody: React.FC<{ title: string | null; description: string; children?: any }> = ({title, description, children}) => {
    return (
        <>
            {title && <ReactMarkdown className="text-lg pb-2 pt-8 font-semibold">{title}</ReactMarkdown>}
            <ReactMarkdown className="mb-4 py-1 text-base">{description}</ReactMarkdown>
            {children}
        </>
    )

}

export const Card: React.FC<{ imagePath: string; coverImage?: boolean; externalImage?: boolean, children: any }> = ({imagePath, coverImage = true, externalImage = true, children}) => {
    return (
        <div className="w-full rounded-xl pb-2 mb-6 px-4 flex flex-col">
            <div className="relative w-full h-56 rounded-xl justify-center">
                <Image
                    fill
                    className={`rounded-xl ${coverImage ? 'object-cover' : 'object-contain'}`}
                    src={externalImage ? getImageUrl(imagePath): imagePath}
                    alt="response"
                    layout={"fixed"}
                />
            </div>
            <div>
                {children}
            </div>
        </div>
    )
}