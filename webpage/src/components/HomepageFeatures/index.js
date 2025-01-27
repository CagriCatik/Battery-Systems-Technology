import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Fundamentals of Battery Technology',
    description: (
      <>
        Learn the basics of battery chemistry, structure, and functionality to understand their role in modern energy systems.{' '}
        <a href="/Battery-Systems-Technology/docs/theory/fundamentals/getting-started" target="_self" style={{ textDecoration: 'underline', color: '#007bff' }}>
          Read more
        </a>
      </>
    ),
  },
  {
    title: 'Aging and Degradation',
    description: (
      <>
        Explore the factors affecting battery aging and degradation and strategies to mitigate performance losses.{' '}
        <a href="/Battery-Systems-Technology/docs/theory/aging_degradation/getting-started" target="_self" style={{ textDecoration: 'underline', color: '#007bff' }}>
          Read more
        </a>
      </>
    ),
  },
  {
    title: 'Chemistry and Design Principles',
    description: (
      <>
        Understand various battery chemistries and principles of designing efficient battery systems.{' '}
        <a href="/Battery-Systems-Technology/docs/theory/chemistry_design_principles/getting-started" target="_self" style={{ textDecoration: 'underline', color: '#007bff' }}>
          Read more
        </a>
      </>
    ),
  },
  {
    title: 'Battery Pack Engineering',
    description: (
      <>
        Dive into the design and integration of battery packs for various applications, ensuring safety and reliability.{' '}
        <a href="/Battery-Systems-Technology/docs/theory/battery_pack/getting_started" target="_self" style={{ textDecoration: 'underline', color: '#007bff' }}>
          Read more
        </a>
      </>
    ),
  },
  {
    title: 'Thermal Management',
    description: (
      <>
        Learn techniques for managing heat generation and dissipation to maintain battery efficiency and safety.{' '}
        <a href="/Battery-Systems-Technology/docs/theory/thermal_management/getting_started" target="_self" style={{ textDecoration: 'underline', color: '#007bff' }}>
          Read more
        </a>
      </>
    ),
  },
  {
    title: 'Characteristics and Technical Specifications',
    description: (
      <>
        Understand key technical specifications such as energy density, power density, and cycle life.{' '}
        <a href="/Battery-Systems-Technology/docs/theory/battery_characteristics/getting_started" target="_self" style={{ textDecoration: 'underline', color: '#007bff' }}>
          Read more
        </a>
      </>
    ),
  },
  {
    title: 'Sizing and Optimization',
    description: (
      <>
        Optimize battery size and capacity to meet specific application requirements and performance goals.{' '}
        <a href="/Battery-Systems-Technology/docs/theory/battery_sizing/getting_started" target="_self" style={{ textDecoration: 'underline', color: '#007bff' }}>
          Read more
        </a>
      </>
    ),
  },
  {
    title: 'Battery Management System',
    description: (
      <>
        Learn about BMS features, including monitoring, balancing, and safety mechanisms for batteries.{' '}
        <a href="/Battery-Systems-Technology/docs/theory/bms/getting_started" target="_self" style={{ textDecoration: 'underline', color: '#007bff' }}>
          Read more
        </a>
      </>
    ),
  },
  {
    title: 'BMS Design and Architecture',
    description: (
      <>
        Explore the architecture and design considerations for developing a robust battery management system.{' '}
        <a href="/Battery-Systems-Technology/docs/theory/bms_architecture/getting_started" target="_self" style={{ textDecoration: 'underline', color: '#007bff' }}>
          Read more
        </a>
      </>
    ),
  },
  {
    title: 'Modeling and Testing',
    description: (
      <>
        Study methods for battery modeling and testing to predict performance and ensure quality control.{' '}
        <a href="/Battery-Systems-Technology/docs/theory/modeling_testing/getting_started" target="_self" style={{ textDecoration: 'underline', color: '#007bff' }}>
          Read more
        </a>
      </>
    ),
  },
];


function Feature({ title, description }) {
  return (
    <div className={clsx(styles.featureBox)}>
      <div className={styles.featureContent}>
        <Heading as="h3" className={styles.featureTitle}>
          {title}
        </Heading>
        <p className={styles.featureDescription}>{description}</p>
      </div>
    </div>
  );
}

export default function BmsFeatures() {
  return (
    <section className={styles.features}>
      {FeatureList.map((props, idx) => (
        <Feature key={idx} {...props} />
      ))}
    </section>
  );
}
