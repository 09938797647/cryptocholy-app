'use client';

import React from 'react';
import styles from './style.module.scss';


const LoaderDot = () => {
    return (
        <span className={`${styles.dot} w-5 h-5 bg-dark-85 dark:bg-white rounded-full block z-20`}></span>
    )
}


export const Loader = () => {
    return (
        <div className="fixed inset-0 flex items-center justify-center bg-white dark:bg-dark-85 bg-opacity-50">
            <div className="flex space-x-5">
                <LoaderDot/>
                <LoaderDot/>
                <LoaderDot/>
                <LoaderDot/>
            </div>
        </div>
    )
}