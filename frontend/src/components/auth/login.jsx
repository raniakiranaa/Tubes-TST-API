"use client"
import React, { useState } from 'react';
import axios from 'axios';
import registerIcon from '../../../public/icons/register.svg';
import Image from 'next/image';
import { useRouter } from 'next/navigation';

const Login = () => {
    // username, password
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const router = useRouter();

    const onSubmit = async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        try {
            const response = await axios.post("https://smartcartchatbot.azurewebsites.net/auth/token",
                formData,
            );

            // get token, restore in storage
            const token = response.data.access_token;

            sessionStorage.setItem("token", token);
            sessionStorage.setItem("username", username);

            console.log(sessionStorage.getItem("token"));
            console.log("username: " + sessionStorage.getItem("username"));

            // route to home page 
            router.push("/chat");

        } catch (err) {
            console.log(err);
            router.push("login?message=Unauthorized");
        }
    }


    return (
        <div className="grid grid-cols-2 shadow-md sm:rounded-lg" style = {{ backgroundColor: '#F9FFFF', position: 'fixed', width: '900px', height: '420px'}}>
            <div>
                <h1 className="pt-20 px-40 text-black semibold-24">Welcome!</h1>
                <div className="ml-12 mt-8" style={{height: '20px', width: '360px'}}>
                    <form className="animate-in flex-1 flex flex-col w-full justify-center text-foreground" onSubmit={ onSubmit }>
                        <input
                            className="rounded-md px-2 py-2 bg-inherit border mb-3 text-gray-500 regular-14"
                            type="username"
                            placeholder="Enter your username"
                            onChange={(event) => {setUsername(event.target.value)}}
                            required
                        />
                        <input
                            className="rounded-md px-2 py-2 bg-inherit border mb-3 text-gray-500 regular-14 peer invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500"
                            type="password"
                            placeholder="Enter your password"
                            onChange={(event) => {setPassword(event.target.value)}}
                            required
                            // maxLength={5}
                        />
                        {/* <span className="hidden text-sm mb-2 text-red-500 regular-12 peer-[&:not(:placeholder-shown):not(:focus):invalid]:block">
                            Data exceeds the maximal length of 25.
                        </span> */}
                        <button type="submit" className="btn_blue rounded-md px-2 py-2 semibold-16 mb-3">Submit</button>
                        <div className="flexCenter regular-14 text-gray-500">
                            <div className="mr-2">
                                Don't have an account? 
                            </div>
                            <a href="/register" className="text-blue-500">Register</a>
                        </div>
                    </form>
                </div>
            </div>

            <div className="pt-20 px-20">
                <Image src={ registerIcon } alt="Register Icon" width={300} height={300}/>
            </div>

        </div>
    )
}

export default Login;