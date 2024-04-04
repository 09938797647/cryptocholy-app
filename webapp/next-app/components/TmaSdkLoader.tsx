'use client';

import React, { PropsWithChildren } from 'react';
import {SDKProvider, DisplayGate} from '@tma.js/sdk-react';
import {Card, CardCenterWrapper} from "./Card";
import Image from "next/image";
import {Loader} from "./Loader/Loader";

interface SDKProviderErrorProps {
  error: unknown;
}

function SDKProviderError({ error }: SDKProviderErrorProps) {
  return (
    <div>
      <CardCenterWrapper>
            <Card key={"quiz-completed"} imagePath='/thinking-face.png' coverImage={false} externalImage={false}>
                <p className="text-center text-[24px]">Holly crap, it happened again</p>
            </Card>
        </CardCenterWrapper>
      <blockquote>
        <code>
          {error instanceof Error
            ? error.message
            : JSON.stringify(error)}
        </code>
      </blockquote>
    </div>
  );
}

const AppInitialState = () => {
    return (
        <div className='flex justify-center content-center items-center h-screen w-full'>
            {/*<Image src={'/zerohero.png'} alt={'zerohero'} height={64} width={64} className="w-16 h-16 rounded-xl"/>*/}
        </div>
    )
}

function SDKProviderLoading() {
  return <Loader/>;
}

function SDKInitialState() {
  return <AppInitialState/>;
}

/**
 * Root component of the whole project.
 */
export function TmaSDKLoader({ children }: PropsWithChildren) {
  return (
    <SDKProvider options={{ cssVars: true, acceptCustomStyles: true, async: true }}>
      <DisplayGate
        error={SDKProviderError}
        loading={SDKProviderLoading}
        initial={SDKInitialState}
      >
        {children}
      </DisplayGate>
    </SDKProvider>
  );
}
