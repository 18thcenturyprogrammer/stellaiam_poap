import React, { Component } from "react";
import ReactDOM from "react-dom/client";
import {BrowserRouter as Router, Routes, Route, Link, Redirect} from "react-router-dom";
import { Container } from 'semantic-ui-react';


import Main from "./Main";
import CreatePoap from "./CreatePoap";
import SendPoapDirect from "./SendPoapDirect";
import SendPoapNonDirect from "./SendPoapNonDirect";






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

							


							
                            {/* <Route path="/content/get/:id" element ={<ContentGet />} />
							<Route path="/content_with_vote/get/:id" element ={<ContentWithVoteGet />} />

							<Route path="/test/web3_storage1" element ={<TestWeb3Storage1 />} /> */}


							{/* <Route path="/show-prices" element ={<ShowPrices />} />
							<Route path="/show-prices-separated-table" element ={<ShowPricesSeparatedTable2 />} />
							<Route path="/test1" element ={<GetAddressBalanceOfUSDT />} />
							<Route path="/monitor-prices" element ={<MonitorPrices />} />
							<Route path="/monitor-prices2" element ={<MonitorPrices2 tokens_and_paths ={this.state.tokens_and_paths}/>} />
							<Route path="/monitor-prices3" element ={<MonitorPrices3 tokens_and_paths ={this.state.tokens_and_paths}/>} />
							

							<Route path="/auth-test" element ={<AuthTest />} />
							<Route path="/signup-test" element ={<SignUpTest />} />
							<Route path="/monitor-prices" element ={<MonitorPrices />} />

							<Route path='/prices_screen1' element = {<PricesScreen1 />} />


							<Route path='/swaptest' element = {<SwapTest />} />
							<Route path='/swaptest2' element = {<SwapTest2 />} />
							<Route path='/swaptest3' element = {<SwapTest3 />} /> */}
							
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
