import {Bounce, toast} from "react-toastify";

const API_URL = process.env.NEXT_PUBLIC_API_URL

const getHeaders = () => {
    return {
        'Authorization': `tma ${sessionStorage.getItem('userData')}`,
        'Content-Type': 'application/json'
    };
};

const handleError = (error: any) => {
    console.error('Error:', error)
    // Display a notification that something went wrong
    toast.error('Blockchain crashed ┬┴┬┴┤( ͡° ͜ʖ├┬┴┬┴', {
        position: "bottom-left",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
        transition: Bounce,
        toastId: 'api-error'
    });
}

// const makeApiCall = async () => {
//     let url = `${API_URL}/`
//
//     const data = fetch(
//         url,
//         {headers: getHeaders()}
//     ).then(response => {
//             if (!response.ok) {
//                 throw new Error('Failed');
//             }
//             return response.json()
//         }
//     ).catch(handleError);
//     return await data;
// };
