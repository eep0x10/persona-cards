import { useEffect, useRef } from 'react';
import { animate, createScope, stagger } from 'animejs';

/** Each effect owns its paper or tray transforms and reverts interrupted motion. */
export function useCardMotion({ root, family, index, back, view, reduced, pulse, selectionSource }) {
  const previous = useRef(null);
  const count = useRef(0);
  useEffect(() => {
    const old = previous.current;
    const flip = old && old.family === family && old.index === index && old.back !== back;
    const direction = old?.family === family && index < old.index ? -1 : 1;
    previous.current = { family, index, back };
    const scope = createScope({ root }).add(() => {
      if (reduced || view !== 'table') return;
      animate('.hand > .active-card', flip ? {
        rotateY: [back ? -85 : 85, 0], translateZ: [28, 0],
        duration: 440, ease: 'out(3)'
      } : {
        translateX: [direction * 44, 0], translateY: [12, 0],
        translateZ: [45, 0], rotateY: [direction * -13, 0],
        rotateZ: [direction * 2.5, 0], scale: [0.97, 1],
        duration: 390, ease: 'out(3)'
      });
      if (!flip) {
        animate('.neighbor-motion', {
          translateX: [direction * 17, 0], translateY: [12, 0],
          rotateZ: [direction * 2, 0], duration: 380,
          delay: stagger(22), ease: 'out(3)'
        });
        animate('.family-navigation button[aria-current] .step-number', {
          scale: [0.88, 1], duration: 260, ease: 'out(3)'
        });
      }
      count.current += 1;
      root.current?.setAttribute('data-motion-count', String(count.current));
    });
    return () => scope.revert();
  }, [family, index, back, view, reduced]);

  useEffect(() => {
    if (!pulse) return;
    const source = selectionSource.current;
    selectionSource.current = null;
    let flight;
    const scope = createScope({ root }).add(() => {
      if (reduced) return;
      const target = root.current?.querySelector('.tray-slot.just-chosen,.optional-choice.just-chosen');
      if (source && target) {
        const end = target.getBoundingClientRect();
        flight = source.node;
        flight.className = 'active-card selection-flight';
        flight.setAttribute('aria-hidden', 'true');
        flight.inert = true;
        Object.assign(flight.style, {
          position: 'fixed', left: `${source.rect.left}px`, top: `${source.rect.top}px`,
          width: `${source.rect.width}px`, height: `${source.rect.height}px`,
          margin: '0', transform: 'none'
        });
        root.current.append(flight);
        animate(flight, {
          translateX: [0, end.left + end.width / 2 - source.rect.left - source.rect.width / 2],
          translateY: [0, end.top + end.height / 2 - source.rect.top - source.rect.height / 2],
          scale: [1, Math.min(end.width / source.rect.width, end.height / source.rect.height)],
          rotateZ: [-5, 0], opacity: [0.95, 0],
          duration: 470, ease: 'inOut(3)'
        });
      }
      animate('.tray-slot.just-chosen,.optional-choice.just-chosen', {
        translateY: [-17, 0], rotateZ: [-3, 0], scale: [1.08, 1],
        duration: 430, delay: source ? 130 : 0, ease: 'out(3)'
      });
    });
    return () => {
      scope.revert();
      flight?.remove();
    };
  }, [pulse, reduced]);
}
