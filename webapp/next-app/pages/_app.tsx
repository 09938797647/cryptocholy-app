import "../styles/globals.css";
import type {AppProps} from "next/app";
import {Bounce, ToastContainer} from "react-toastify";
import 'react-toastify/dist/ReactToastify.min.css';
import {TmaSDKLoader} from "../components/TmaSdkLoader";
import {Inter} from 'next/font/google';
import PlausibleProvider from 'next-plausible';

const inter = Inter({subsets: ['cyrillic-ext', 'latin-ext']});

export default function MyApp({Component, pageProps}: AppProps) {
    return (
        <div className={inter.className}>
            <TmaSDKLoader>
                <PlausibleProvider domain="quiz.joincommunity.xyz" selfHosted scriptProps={{
                    src: 'https://plausible.joincommunity.xyz/js/script.js',
                    // @ts-ignore
                    "data-api": "https://plausible.joincommunity.xyz/api/event",
                }}>
                    <Component {...pageProps} />
                    <ToastContainer
                        position="bottom-left"
                        autoClose={3000}
                        limit={1}
                        hideProgressBar={false}
                        newestOnTop
                        closeOnClick
                        rtl={false}
                        pauseOnFocusLoss
                        draggable
                        pauseOnHover
                        theme="dark"
                        transition={Bounce}
                    />
                </PlausibleProvider>
            </TmaSDKLoader>
        </div>
    )
}
