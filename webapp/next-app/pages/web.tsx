import React, {useEffect, useMemo, useReducer} from 'react';
import {useInitData, useInitDataRaw, useMainButton, useMiniApp, useViewport} from "@tma.js/sdk-react";
import {Loader} from "../components/Loader/Loader";
import {useLoader} from "../hooks/loader";

// Define the states of your application
const states = {
    INIT: 'INIT',
    ERROR: 'ERROR',
};

// Define the actions that can be performed
const actions = {
    INITIALIZE: 'INITIALIZE',
    HANDLE_ERROR: 'HANDLE_ERROR',
};

// Define the initial state
const initialState = {
    state: states.INIT,
    quizDetails: null,
    details: null,
    isLoading: false,
    isError: false,
};

// Define the reducer
const reducer = (state, action) => {
    switch (action.type) {
        case actions.HANDLE_ERROR:
            return {...state, state: states.ERROR, isError: true, isLoading: false};
        default:
            return state;
    }
};

const WebApp = () => {
    const [state, dispatch] = useReducer(reducer, initialState);
    const {state: appState, quizDetails, details, isLoading} = state;

    const mainButton = useMainButton();
    const miniApp = useMiniApp();
    const initData = useInitData();
    const initDataRaw = useInitDataRaw();
    const viewport = useViewport();

    const renderLoader = useLoader(isLoading)
    // const translations = useTranslation(initData.user.languageCode)

    useEffect(() => {
        updateBackgroundColor()
        viewport.expand()
        miniApp.ready()
        // dispatch({type: actions.FETCH});
        sessionStorage.setItem('userData', initDataRaw)
    }, []);

    const updateBackgroundColor = () => {
        miniApp.setBackgroundColor("#ffffff")
    };

    const disableMainButton = () => {
        mainButton.hideLoader()
        mainButton.hide()
    };

    const enableMainButton = (text: string) => {
        mainButton.hideLoader()
        mainButton.setText(text).show()
    };

    // const fetchQuestionData = useCallback(async (questionId: number | null = null) => {
    //     dispatch({type: actions.FETCH_QUESTION_DATA});
    //     try {
    //         const data = await getQuestion(initData.startParam, questionId);
    //         if (data.quiz.question === null) {
    //             dispatch({type: actions.FINISH_QUIZ, quizDetails: data.quiz, details: null});
    //         } else {
    //             dispatch({
    //                 type: isInitialized ? actions.FETCH_QUESTION_DATA_SUCCESS : actions.INITIALIZE,
    //                 quizDetails: data.quiz,
    //                 details: data.details
    //             });
    //         }
    //     } catch (error) {
    //         dispatch({type: isInitialized ? actions.FETCH_QUESTION_DATA_FAILURE : actions.HANDLE_ERROR});
    //     }
    // }, [initData.startParam, isInitialized]);

    // useEffect(() => {
    //     if (appState === states.LOADING || appState === states.INIT) {
    //         fetchQuestionData(details?.nextQuestionId || null);
    //     }
    // }, [appState, details, fetchQuestionData]);

    const renderCard = useMemo(() => {
        return <></>
    }, [])

    return (
        <>
            {
                quizDetails && (
                    <div className="flex justify-center min-h-screen dark:text-white">
                        <div className="flex flex-col max-w-lg gap-y-4 pt-4 w-full sm:w-[600px]">
                            {renderCard}
                        </div>
                    </div>
                )
            }
            {renderLoader && <Loader/>}
        </>
    )
};

export default WebApp;
