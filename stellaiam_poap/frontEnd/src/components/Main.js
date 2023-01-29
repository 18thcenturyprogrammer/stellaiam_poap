import React from "react";
import { AnimationOnScroll } from 'react-animation-on-scroll';

import { MDBIcon } from "mdb-react-ui-kit";

import Menu from "./Menu";
import HeroImage from "./HeroImage";
import HeroCarousel from "./HeroCarousel";
import LeftImgFeature from "./LeftImgFeature";
import LeftImgFeature2 from "./LeftImgFeature2";
import RightImgFeature from "./RightImgFeature";
import PriceCards from "./PriceCards";
import Faq from "./Faq";
import Footer from "./Footer";

const Main = ()=>{

    return(

        <>
            <Menu updateProvider={()=>{}} updateCurrentAccount={()=>{}} updateChainId={()=>{}} />
            <HeroCarousel />

            <h2 className="ui horizontal divider header">
                <i className="question circle icon text-primary"></i>
                &nbsp; What & Why & How &nbsp;
                <i className="exclamation icon text-primary"></i>
            </h2>

            <AnimationOnScroll animateIn="animate__fadeInLeftBig">
                <LeftImgFeature />
            </AnimationOnScroll>

            <AnimationOnScroll animateIn="animate__fadeInRightBig">
                <RightImgFeature />
            </AnimationOnScroll>

            <AnimationOnScroll animateIn="animate__fadeInLeftBig">
                <LeftImgFeature2 />
            </AnimationOnScroll>

            <h2 className="ui horizontal divider header">
                <i className="tags icon text-primary"></i>
                &nbsp; 가격 &nbsp;
                <i className="tags text-primary"></i>
            </h2>

            <AnimationOnScroll animateIn="animate__rubberBand">
                <PriceCards />
            </AnimationOnScroll>

            <div className="ui divider"></div>

            <div id="Faq" className="ui two column grid">
                <div id="firstCol" className="three wide column right aligned">
                    <div className="ui">
                        <h2>
                            <i className="question icon text-primary"></i>
                            &nbsp; Q & A &nbsp;
                        </h2>
                    </div>
                </div>
                <div id="firstCol" className="thirteen wide column">
                    <div className="ui">
                    <Faq />
                    </div>
                </div>
            
            </div>
            
                
                
                
            
            
            

            <Footer />
            
        </>

    );

};

export default Main;