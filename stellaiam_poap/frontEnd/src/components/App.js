import React, { Component } from "react";
import ReactDOM from "react-dom/client";
import {BrowserRouter as Router, Routes, Route, Link, Redirect} from "react-router-dom";
import { Container } from 'semantic-ui-react';


import Main from "./Main";
import CreatePoap from "./CreatePoap";
import {SendPoapDirect} from "./SendPoapDirect";
import {SendPoapNonDirect} from "./SendPoapNonDirect";
import { ReceivePoap } from "./ReceivePoap";







export default class App extends Component{

	
	
	

	constructor(props) {
		super(props)

		
	}


	render (){
		

		return (
			
			
				<Container>
					<Router>
						<Routes>
							<Route exact path="/" element ={<Main />} />
							<Route exact path="/create_poap" element ={<CreatePoap />} />
							<Route exact path="/send_poap_direct" element ={<SendPoapDirect />} />
							<Route exact path="/send_poap_non_direct" element ={<SendPoapNonDirect />} />
							<Route path="/receive_poap/:id" element ={<ReceivePoap />} />
							
						</Routes>
					</Router>
				</Container>
				
			
		);

	}
}


const appDiv = document.getElementById("app");

// new way render root ref) https://stackoverflow.com/a/73439099
const root = ReactDOM.createRoot(appDiv);

root.render(<App />);
