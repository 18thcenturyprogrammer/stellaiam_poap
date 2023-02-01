import React from 'react';
import {
  MDBCarousel,
  MDBCarouselItem,
} from 'mdb-react-ui-kit';

export default function HeroCarousel() {
  return (
    <MDBCarousel id="HeroCarousel" showControls dark showIndicators>
      <MDBCarouselItem
        className='w-100 d-block'
        itemId={1}
        src='static/for_react/images/hero1.png'
        alt='...'
      >
        
        <h3><i className="rocket icon"></i>&nbsp;즐거운 순간, 행복한 순간을 기억하세요</h3>
        <p>각종 이벤트 참여의 기억을 되살리는 기념품을 만들어 보세요</p>
      </MDBCarouselItem>
      <MDBCarouselItem
        className='w-100 d-block'
        itemId={2}
        src='static/for_react/images/hero2.png'
        alt='...'
      >
        <h3><i className="gift icon"></i>&nbsp;남들과 다른 색다른 선물</h3>
        <p>특별한 사람에게 개성있는 선물을 드려보세요</p>
        <p>NFT 카드, 내가그린 그림, 오래도록 기억남을 한문장을 선물해 보세요</p>
      </MDBCarouselItem>
      <MDBCarouselItem
        className='w-100 d-block'
        itemId={3}
        src='static/for_react/images/hero3.png'
        alt='...'
      >
        <h3><i className="trophy icon"></i>&nbsp;전혀 다른 인증서를 만들어 보세요</h3>
        <p>POAP로 교육과정이수, 자격증, 졸업장을 만드세요</p>
      </MDBCarouselItem>
    </MDBCarousel>
  );
}