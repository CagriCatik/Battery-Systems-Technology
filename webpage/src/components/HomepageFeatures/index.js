import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

// 1. Update FeatureList items to describe BMS features
const FeatureList = [
  {
    title: 'Battery Monitoring',
    // Swap out the SVG below for something relevant to batteries
    //Svg: require('@site/static/img/undraw_battery_level.svg').default,
    description: (
      <>
        Monitor battery voltage, current, temperature, and overall health in real-time, ensuring safe and optimal performance.
      </>
    ),
  },
  {
    title: 'Cell Balancing',
    //Svg: require('@site/static/img/undraw_balance.svg').default,
    description: (
      <>
        Keep cells at a similar state of charge to maximize battery lifetime and capacity, preventing premature wear or damage.
      </>
    ),
  },
  {
    title: 'Alerts & Notifications',
    //Svg: require('@site/static/img/undraw_alert.svg').default,
    description: (
      <>
        Receive notifications for overcharge, overheating, low voltage, and other critical conditions—enabling proactive maintenance.
      </>
    ),
  },
];

// 2. The Feature component can remain the same, just referencing your new data
function Feature({ Svg, title, description }) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        {Svg && <Svg className={styles.featureSvg} role="img" />}
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

// 3. Optionally rename the exported function to "BmsFeatures" or keep it "HomepageFeatures"
export default function BmsFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
